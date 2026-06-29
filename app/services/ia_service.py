import re
from app.services.sla_service import obtener_sla_minutos

REGLAS = [
    {
        "prioridad": "Crítica",
        "area": "Infraestructura",
        "equipo": "NOC Nivel 2",
        "confianza": 96.8,
        "palabras": [
            "caída", "caido", "caído", "servidor", "producción", "produccion",
            "facturación", "facturacion", "base de datos", "no responde",
            "servicio detenido", "sistema detenido", "principal sin conexión"
        ],
    },
    {
        "prioridad": "Alta",
        "area": "Redes",
        "equipo": "Equipo de Redes",
        "confianza": 91.2,
        "palabras": ["vpn", "conexión", "conexion", "red", "internet", "latencia", "usuarios remotos"],
    },
    {
        "prioridad": "Alta",
        "area": "Soporte Técnico",
        "equipo": "Mesa de Ayuda",
        "confianza": 88.5,
        "palabras": ["inicio sesión", "inicio de sesión", "login", "acceso", "credenciales", "bloqueado"],
    },
    {
        "prioridad": "Media",
        "area": "Desarrollo",
        "equipo": "Soporte Aplicaciones",
        "confianza": 79.3,
        "palabras": ["crm", "aplicación", "aplicacion", "error", "módulo", "modulo", "lento", "lentitud"],
    },
    {
        "prioridad": "Media",
        "area": "Base de Datos",
        "equipo": "DBA Team",
        "confianza": 82.0,
        "palabras": ["consulta sql", "postgresql", "tabla", "query", "base de datos", "registro duplicado"],
    },
]


def _normalizar(texto: str) -> str:
    return texto.lower().strip()


def extraer_palabras_clave(texto: str) -> list[str]:
    palabras = re.findall(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ0-9]+", texto.lower())
    ignorar = {"el", "la", "los", "las", "un", "una", "de", "del", "en", "con", "por", "para", "que", "no", "al", "se", "y", "o"}
    limpias = [p for p in palabras if len(p) > 3 and p not in ignorar]
    # Mantiene orden y evita duplicados.
    return list(dict.fromkeys(limpias))[:10]


def analizar_ticket_ia(titulo: str, descripcion: str) -> dict:
    texto = _normalizar(f"{titulo} {descripcion}")
    coincidencias = []

    mejor_regla = None
    mejor_score = -1

    for regla in REGLAS:
        score = 0
        for palabra in regla["palabras"]:
            if palabra in texto:
                score += 1
                coincidencias.append(palabra)
        if score > mejor_score:
            mejor_score = score
            mejor_regla = regla

    if mejor_score <= 0 or mejor_regla is None:
        resultado = {
            "prioridad": "Baja",
            "area": "Soporte Técnico",
            "equipo": "Mesa de Ayuda",
            "confianza": 68.0,
        }
    else:
        ajuste = min(mejor_score * 2.5, 8)
        resultado = {
            "prioridad": mejor_regla["prioridad"],
            "area": mejor_regla["area"],
            "equipo": mejor_regla["equipo"],
            "confianza": min(99.0, round(mejor_regla["confianza"] + ajuste, 2)),
        }

    keywords = list(dict.fromkeys(coincidencias + extraer_palabras_clave(texto)))[:12]
    resultado["palabras_clave"] = ", ".join(keywords) if keywords else "sin palabras clave relevantes"
    resultado["sla_minutos"] = obtener_sla_minutos(resultado["prioridad"])
    resultado["modelo"] = "SmartPriority NLP v1.0"
    return resultado
