from datetime import datetime

from app.database.conexion import conexion_bd
from app.models.tickets import TICKETS_DEMO
from app.services.ia_service import analizar_ticket_ia
from app.services.sla_service import calcular_vencimiento, tiempo_restante, formatear_sla


class TicketError(Exception):
    pass


def _ticket_demo_formateado(ticket: dict) -> dict:
    return ticket


def listar_tickets() -> list[dict]:
    """Lista tickets desde la vista PostgreSQL. Si falla, usa datos demo."""
    try:
        with conexion_bd() as cursor:
            cursor.execute("SELECT * FROM vista_tickets ORDER BY fecha_registro DESC")
            filas = cursor.fetchall()
        return [_formatear_ticket_vista(fila) for fila in filas]
    except Exception:
        return [_ticket_demo_formateado(t) for t in TICKETS_DEMO]


def _formatear_ticket_vista(fila: dict) -> dict:
    vencimiento = fila.get("vencimiento_sla")
    confianza = fila.get("porcentaje_confianza") or 0
    return {
        "id_ticket": fila.get("id_ticket"),
        "id": fila.get("codigo_ticket") or f"TK-{fila.get('id_ticket', 0):05d}",
        "titulo": fila.get("titulo") or "Sin título",
        "descripcion": fila.get("descripcion") or "",
        "categoria": fila.get("area") or "Sin área",
        "prioridad": fila.get("prioridad") or "Media",
        "estado": fila.get("estado") or "Pendiente",
        "sla": tiempo_restante(vencimiento),
        "confianza": float(confianza),
        "equipo": fila.get("equipo_sugerido") or "Sin asignar",
        "fecha": _fecha_corta(fila.get("fecha_registro")),
        "solicitante": fila.get("solicitante") or "Sin solicitante",
        "estado_validacion": fila.get("estado_validacion") or "Pendiente",
        "area_sugerida": fila.get("area_sugerida") or "",
        "prioridad_sugerida": fila.get("prioridad_sugerida") or "",
        "vencimiento_sla": vencimiento,
    }


def _fecha_corta(fecha) -> str:
    if not fecha:
        return "Sin fecha"
    if isinstance(fecha, str):
        return fecha[:16]
    return fecha.strftime("%d/%m/%Y %H:%M")


def obtener_catalogos() -> dict:
    try:
        with conexion_bd() as cursor:
            cursor.execute("SELECT id_area, nombre FROM areas WHERE estado = TRUE ORDER BY nombre")
            areas = cursor.fetchall()
            cursor.execute("SELECT id_prioridad, nombre, nivel FROM prioridades ORDER BY nivel")
            prioridades = cursor.fetchall()
            cursor.execute("SELECT id_equipo, nombre FROM equipos WHERE estado = TRUE ORDER BY nombre")
            equipos = cursor.fetchall()
        return {"areas": areas, "prioridades": prioridades, "equipos": equipos}
    except Exception:
        return {
            "areas": [{"nombre": n} for n in ["Soporte Técnico", "Redes", "Desarrollo", "Infraestructura", "Base de Datos"]],
            "prioridades": [{"nombre": n} for n in ["Crítica", "Alta", "Media", "Baja"]],
            "equipos": [{"nombre": n} for n in ["Mesa de Ayuda", "Equipo de Redes", "Soporte Aplicaciones", "NOC Nivel 2", "DBA Team"]],
        }


def previsualizar_analisis(titulo: str, descripcion: str) -> dict:
    return analizar_ticket_ia(titulo, descripcion)


def crear_ticket(titulo: str, descripcion: str, id_usuario: int, area_manual: str | None = None) -> dict:
    """Crea un ticket, analiza con IA y guarda la derivación sugerida."""
    if not titulo.strip() or not descripcion.strip():
        raise TicketError("El título y la descripción son obligatorios.")

    analisis = analizar_ticket_ia(titulo, descripcion)
    area_nombre = area_manual or analisis["area"]
    prioridad_nombre = analisis["prioridad"]
    equipo_nombre = analisis["equipo"]
    vencimiento = calcular_vencimiento(prioridad_nombre)

    try:
        with conexion_bd(commit=True) as cursor:
            id_area = _obtener_id(cursor, "areas", "id_area", area_nombre, valor_defecto="Soporte Técnico")
            id_prioridad = _obtener_id(cursor, "prioridades", "id_prioridad", prioridad_nombre, valor_defecto="Media")

            cursor.execute(
                """
                INSERT INTO tickets (
                    titulo, descripcion, estado, id_usuario, id_area, id_prioridad, vencimiento_sla
                )
                VALUES (%s, %s, 'Analizado por IA', %s, %s, %s, %s)
                RETURNING id_ticket, codigo_ticket
                """,
                (titulo.strip(), descripcion.strip(), id_usuario, id_area, id_prioridad, vencimiento),
            )
            nuevo = cursor.fetchone()
            id_ticket = nuevo["id_ticket"]

            cursor.execute(
                """
                INSERT INTO analisis_ia (
                    id_ticket, palabras_clave, prioridad_sugerida, area_sugerida,
                    equipo_sugerido, porcentaje_confianza, modelo_utilizado,
                    estado_validacion, observacion_operador
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pendiente', %s)
                """,
                (
                    id_ticket,
                    analisis["palabras_clave"],
                    prioridad_nombre,
                    analisis["area"],
                    equipo_nombre,
                    analisis["confianza"],
                    analisis["modelo"],
                    "Ticket pendiente de validación por operador.",
                ),
            )

            id_equipo = _obtener_id(cursor, "equipos", "id_equipo", equipo_nombre, puede_ser_none=True)
            id_tecnico = _tecnico_disponible(cursor)
            if id_equipo and id_tecnico:
                cursor.execute(
                    """
                    INSERT INTO asignaciones (id_ticket, id_tecnico, id_equipo)
                    VALUES (%s, %s, %s)
                    """,
                    (id_ticket, id_tecnico, id_equipo),
                )

            cursor.execute(
                """
                INSERT INTO historial (id_ticket, id_usuario, accion, estado_anterior, estado_nuevo, observacion)
                VALUES
                (%s, %s, 'Creación de ticket', NULL, 'Pendiente', 'Ticket registrado desde la interfaz'),
                (%s, %s, 'Análisis IA', 'Pendiente', 'Analizado por IA', %s)
                """,
                (
                    id_ticket,
                    id_usuario,
                    id_ticket,
                    id_usuario,
                    f"Prioridad sugerida: {prioridad_nombre}. Confianza IA: {analisis['confianza']}%",
                ),
            )

            cursor.execute(
                """
                INSERT INTO actividad_tiempo_real (descripcion, tipo, id_ticket, id_usuario)
                VALUES (%s, 'IA', %s, %s)
                """,
                (f"IA analizó {nuevo['codigo_ticket']} como prioridad {prioridad_nombre}", id_ticket, id_usuario),
            )

        return {"codigo": nuevo["codigo_ticket"], **analisis}
    except Exception as error:
        raise TicketError(f"No se pudo guardar el ticket en PostgreSQL: {error}") from error


def _obtener_id(cursor, tabla: str, columna_id: str, nombre: str, valor_defecto: str | None = None, puede_ser_none: bool = False):
    cursor.execute(f"SELECT {columna_id} FROM {tabla} WHERE nombre = %s LIMIT 1", (nombre,))
    fila = cursor.fetchone()
    if fila:
        return fila[columna_id]
    if valor_defecto:
        cursor.execute(f"SELECT {columna_id} FROM {tabla} WHERE nombre = %s LIMIT 1", (valor_defecto,))
        fila = cursor.fetchone()
        if fila:
            return fila[columna_id]
    if puede_ser_none:
        return None
    raise TicketError(f"No existe el registro '{nombre}' en la tabla {tabla}.")


def _tecnico_disponible(cursor):
    cursor.execute(
        """
        SELECT id_usuario
        FROM usuarios
        WHERE rol = 'Técnico' AND estado = TRUE
        ORDER BY id_usuario
        LIMIT 1
        """
    )
    fila = cursor.fetchone()
    return fila["id_usuario"] if fila else None


def obtener_actividad_reciente(limite: int = 6) -> list[dict]:
    try:
        with conexion_bd() as cursor:
            cursor.execute(
                """
                SELECT descripcion, tipo, fecha
                FROM actividad_tiempo_real
                ORDER BY fecha DESC
                LIMIT %s
                """,
                (limite,),
            )
            return cursor.fetchall()
    except Exception:
        return [
            {"descripcion": "IA clasificó un ticket como crítico", "tipo": "IA", "fecha": "Demo"},
            {"descripcion": "Ticket derivado a NOC Nivel 2", "tipo": "Asignación", "fecha": "Demo"},
            {"descripcion": "SLA actualizado automáticamente", "tipo": "SLA", "fecha": "Demo"},
        ]
