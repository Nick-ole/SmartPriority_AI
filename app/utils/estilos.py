"""Funciones visuales reutilizables para mantener consistencia SaaS/enterprise."""
import customtkinter as ctk
from . import colores as c

FONT = "Inter"
FONT_FALLBACK = "Segoe UI"


def fuente(tamano=13, peso="normal"):
    """Retorna una tupla de fuente. Tkinter usará fallback si Inter no está instalada."""
    return (FONT, tamano, peso)


def crear_card(master, **kwargs):
    params = {
        "fg_color": c.BLANCO,
        "corner_radius": 18,
        "border_width": 1,
        "border_color": c.BORDE,
    }
    params.update(kwargs)
    return ctk.CTkFrame(master, **params)


def crear_boton_primario(master, text, command=None, width=150):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        height=40,
        corner_radius=12,
        fg_color=c.AZUL,
        hover_color="#1D4ED8",
        font=fuente(13, "bold"),
        text_color="white",
    )


def crear_boton_secundario(master, text, command=None, width=150):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        height=40,
        corner_radius=12,
        fg_color="#EEF2FF",
        hover_color="#E0E7FF",
        font=fuente(13, "bold"),
        text_color=c.AZUL_OSCURO,
    )


def etiqueta(master, texto, fondo, color, ancho=90):
    label = ctk.CTkLabel(
        master,
        text=texto,
        fg_color=fondo,
        text_color=color,
        corner_radius=12,
        width=ancho,
        height=26,
        font=fuente(12, "bold"),
    )
    return label
