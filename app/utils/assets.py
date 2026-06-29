"""Utilidades para cargar recursos visuales del proyecto."""
from pathlib import Path


def raiz_proyecto() -> Path:
    return Path(__file__).resolve().parents[2]


def ruta_recurso(*partes: str) -> str:
    """Devuelve una ruta absoluta compatible con Windows/Linux."""
    return str(raiz_proyecto().joinpath(*partes))


def ruta_logo(nombre: str = "logo_blue.png") -> str:
    return ruta_recurso("app", "assets", "icons", nombre)
