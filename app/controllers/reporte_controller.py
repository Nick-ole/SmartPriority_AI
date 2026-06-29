from app.database.conexion import conexion_bd
from app.models.reportes import KPIS as KPIS_DEMO, TICKETS_DIA, CATEGORIAS, EQUIPOS


def obtener_kpis() -> list[tuple[str, str, str, str]]:
    try:
        with conexion_bd() as cursor:
            cursor.execute("SELECT * FROM vista_dashboard")
            d = cursor.fetchone() or {}
        total = int(d.get("total_tickets") or 0)
        activos = int(d.get("tickets_activos") or 0)
        criticos = int(d.get("tickets_criticos") or 0)
        confianza = float(d.get("confianza_promedio_ia") or 0)
        sla_vencido = int(d.get("tickets_sla_vencido") or 0)
        return [
            ("Tickets totales", str(total), "Base activa", "🎫"),
            ("Tickets activos", str(activos), f"{criticos} críticos", "⏱️"),
            ("Confianza IA", f"{confianza:.1f}%", "Promedio NLP", "✨"),
            ("SLA vencido", str(sla_vencido), "Requiere atención", "⚡"),
        ]
    except Exception:
        return KPIS_DEMO


def tickets_por_prioridad() -> list[tuple[str, int]]:
    try:
        with conexion_bd() as cursor:
            cursor.execute(
                """
                SELECT p.nombre, COUNT(t.id_ticket)::int AS total
                FROM prioridades p
                LEFT JOIN tickets t ON p.id_prioridad = t.id_prioridad
                GROUP BY p.nivel, p.nombre
                ORDER BY p.nivel
                """
            )
            return [(f["nombre"], f["total"]) for f in cursor.fetchall()]
    except Exception:
        return [("Crítica", 18), ("Alta", 34), ("Media", 49), ("Baja", 27)]


def actividad_por_dia() -> list[tuple[str, int]]:
    try:
        with conexion_bd() as cursor:
            cursor.execute(
                """
                SELECT TO_CHAR(fecha_registro, 'Dy') AS dia, COUNT(*)::int AS total
                FROM tickets
                WHERE fecha_registro >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY 1, DATE(fecha_registro)
                ORDER BY DATE(fecha_registro)
                """
            )
            datos = [(f["dia"].capitalize(), f["total"]) for f in cursor.fetchall()]
        return datos or TICKETS_DIA
    except Exception:
        return TICKETS_DIA


def tickets_por_categoria() -> list[tuple[str, int]]:
    try:
        with conexion_bd() as cursor:
            cursor.execute(
                """
                SELECT a.nombre, COUNT(t.id_ticket)::int AS total
                FROM areas a
                LEFT JOIN tickets t ON a.id_area = t.id_area
                GROUP BY a.nombre
                ORDER BY total DESC, a.nombre
                """
            )
            return [(f["nombre"], f["total"]) for f in cursor.fetchall()]
    except Exception:
        return CATEGORIAS


def rendimiento_equipos() -> list[tuple[str, str, str, str]]:
    try:
        with conexion_bd() as cursor:
            cursor.execute("SELECT * FROM vista_rendimiento_equipos")
            filas = cursor.fetchall()
        if not filas:
            return EQUIPOS
        datos = []
        for f in filas:
            confianza = float(f.get("confianza_promedio") or 0)
            datos.append((
                f["equipo"],
                f"{confianza:.0f}% IA",
                f"{f.get('tickets_asignados', 0)} asignados",
                str(f.get("tickets_resueltos", 0)),
            ))
        return datos
    except Exception:
        return EQUIPOS
