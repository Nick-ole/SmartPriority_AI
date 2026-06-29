import customtkinter as ctk

from app.controllers.reporte_controller import obtener_kpis, tickets_por_prioridad
from app.controllers.ticket_controller import obtener_actividad_reciente
from app.utils import colores as c
from app.utils.estilos import crear_card, fuente, etiqueta


class PanelPrincipalView(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color=c.FONDO)
        self.usuario = usuario
        self.crear_vista()

    def crear_vista(self):
        cont = ctk.CTkScrollableFrame(self, fg_color=c.FONDO, corner_radius=0)
        cont.pack(fill="both", expand=True, padx=22, pady=18)
        cont.grid_columnconfigure((0, 1, 2, 3), weight=1)

        titulo = ctk.CTkLabel(cont, text="Panel principal", font=fuente(26, "bold"), text_color=c.TEXTO)
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
        subtitulo = ctk.CTkLabel(
            cont,
            text="Resumen ejecutivo conectado a PostgreSQL: tickets, SLA, IA y actividad operativa",
            font=fuente(14),
            text_color=c.TEXTO_SUAVE,
        )
        subtitulo.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 18))

        for i, (nombre, valor, cambio, icono) in enumerate(obtener_kpis()):
            card = crear_card(cont)
            card.grid(row=2, column=i, sticky="nsew", padx=8, pady=8)
            card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(card, text=icono, font=fuente(28), text_color=c.AZUL).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))
            ctk.CTkLabel(card, text=valor, font=fuente(28, "bold"), text_color=c.AZUL_OSCURO).grid(row=1, column=0, sticky="w", padx=18)
            ctk.CTkLabel(card, text=nombre, font=fuente(13), text_color=c.TEXTO_SUAVE).grid(row=2, column=0, sticky="w", padx=18, pady=(0, 8))
            etiqueta(card, cambio, c.VERDE_CLARO if "vencido" not in cambio.lower() else c.ROJO_CLARO, c.VERDE if "vencido" not in cambio.lower() else c.ROJO, 118).grid(row=3, column=0, sticky="w", padx=18, pady=(0, 16))

        analitica = crear_card(cont)
        analitica.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=8, pady=(16, 8))
        analitica.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(analitica, text="Analítica de tickets por prioridad", font=fuente(18, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 14))

        datos_prioridad = tickets_por_prioridad()
        max_val = max([valor for _, valor in datos_prioridad] or [1]) or 1
        for idx, (nombre, valor) in enumerate(datos_prioridad, start=1):
            color = c.PRIORIDAD_COLOR.get(nombre, c.AZUL)
            fila = ctk.CTkFrame(analitica, fg_color="transparent")
            fila.grid(row=idx, column=0, sticky="ew", padx=20, pady=7)
            fila.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(fila, text=nombre, width=90, anchor="w", font=fuente(13, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w")
            barra_bg = ctk.CTkFrame(fila, height=12, fg_color="#EEF2F7", corner_radius=10)
            barra_bg.grid(row=0, column=1, sticky="ew", padx=12)
            ancho = max(40, int((valor / max_val) * 420))
            barra = ctk.CTkFrame(barra_bg, height=12, fg_color=color, corner_radius=10, width=ancho)
            barra.place(x=0, y=0)
            ctk.CTkLabel(fila, text=str(valor), width=42, font=fuente(13, "bold"), text_color=c.TEXTO_SUAVE).grid(row=0, column=2)

        actividad = crear_card(cont)
        actividad.grid(row=3, column=3, sticky="nsew", padx=8, pady=(16, 8))
        ctk.CTkLabel(actividad, text="Actividad en tiempo real", font=fuente(18, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 12))
        colores_tipo = {"IA": c.MORADO, "Ticket": c.AZUL, "Asignación": c.NARANJA, "Derivación": c.VERDE, "Cierre": c.VERDE, "SLA": c.ROJO}
        for evento in obtener_actividad_reciente(6):
            color = colores_tipo.get(evento.get("tipo"), c.AZUL)
            fila = ctk.CTkFrame(actividad, fg_color="transparent")
            fila.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(fila, text="●", text_color=color, font=fuente(18)).pack(side="left", padx=(0, 8))
            bloque = ctk.CTkFrame(fila, fg_color="transparent")
            bloque.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(bloque, text=evento.get("descripcion", "Actividad"), font=fuente(12, "bold"), text_color=c.TEXTO, anchor="w", wraplength=245, justify="left").pack(anchor="w")
            fecha = evento.get("fecha", "")
            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%d/%m %H:%M")
            ctk.CTkLabel(bloque, text=str(fecha), font=fuente(11), text_color=c.TEXTO_SUAVE, anchor="w").pack(anchor="w")

        alertas = crear_card(cont)
        alertas.grid(row=4, column=0, columnspan=4, sticky="ew", padx=8, pady=16)
        alertas.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkLabel(alertas, text="Alertas inteligentes", font=fuente(18, "bold"), text_color=c.TEXTO).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(18, 8))
        tarjetas = [
            ("SLA en riesgo", "Revisa tickets críticos antes del vencimiento del SLA.", c.ROJO_CLARO, c.ROJO),
            ("Priorización activa", "La IA analiza título y descripción para sugerir área, equipo y prioridad.", c.NARANJA_CLARO, c.NARANJA),
            ("PostgreSQL conectado", "Los tickets y reportes se actualizan desde la base de datos.", c.VERDE_CLARO, c.VERDE),
        ]
        for i, (t, d, bg, col) in enumerate(tarjetas):
            alerta = ctk.CTkFrame(alertas, fg_color=bg, corner_radius=14)
            alerta.grid(row=1, column=i, sticky="ew", padx=14, pady=(8, 18))
            ctk.CTkLabel(alerta, text=t, font=fuente(14, "bold"), text_color=col).pack(anchor="w", padx=14, pady=(12, 4))
            ctk.CTkLabel(alerta, text=d, font=fuente(12), text_color=c.TEXTO, wraplength=280, justify="left").pack(anchor="w", padx=14, pady=(0, 12))
