from datetime import datetime, timedelta

SLA_MINUTOS = {
    "Crítica": 30,
    "Alta": 120,
    "Media": 480,
    "Baja": 1440,
}


def obtener_sla_minutos(prioridad: str) -> int:
    return SLA_MINUTOS.get(prioridad, 480)


def calcular_vencimiento(prioridad: str, desde: datetime | None = None) -> datetime:
    desde = desde or datetime.now()
    return desde + timedelta(minutes=obtener_sla_minutos(prioridad))


def formatear_sla(minutos: int | None) -> str:
    if minutos is None:
        return "Sin SLA"
    if minutos < 60:
        return f"{minutos} min"
    horas = minutos // 60
    resto = minutos % 60
    if resto == 0:
        return f"{horas} h"
    return f"{horas} h {resto} min"


def tiempo_restante(vencimiento) -> str:
    if not vencimiento:
        return "Sin SLA"
    ahora = datetime.now(vencimiento.tzinfo) if getattr(vencimiento, "tzinfo", None) else datetime.now()
    delta = vencimiento - ahora
    minutos = int(delta.total_seconds() // 60)
    if minutos < 0:
        return "SLA vencido"
    return formatear_sla(minutos)
