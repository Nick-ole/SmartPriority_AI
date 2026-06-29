import customtkinter as ctk
from tkinter import messagebox

from app.utils import colores as c
from app.utils.estilos import crear_card, crear_boton_primario, fuente, etiqueta
from app.utils.iconos import ICONOS


class FlujoIAView(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color=c.FONDO)
        self.usuario = usuario
        self.crear_vista()

    def crear_vista(self):
        cont = ctk.CTkScrollableFrame(self, fg_color=c.FONDO, corner_radius=0)
        cont.pack(fill="both", expand=True, padx=24, pady=22)
        cont.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(cont, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Flujo inteligente con IA", font=fuente(26, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Proceso de priorización automática mediante NLP, reglas SLA y validación humana", font=fuente(14), text_color=c.TEXTO_SUAVE).grid(row=1, column=0, sticky="w")
        crear_boton_primario(header, "Simular análisis IA", command=self.simular, width=170).grid(row=0, column=1, rowspan=2, padx=8)

        flujo = crear_card(cont)
        flujo.grid(row=1, column=0, sticky="ew")
        flujo.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(flujo, text="Pipeline de atención del ticket", font=fuente(18, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 10))

        scroll_horizontal = ctk.CTkScrollableFrame(flujo, orientation="horizontal", fg_color="transparent", height=260)
        scroll_horizontal.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))

        pasos = [
            (ICONOS["registro"], "Registro de incidencia", "Captura inicial del problema, usuario afectado y canal de entrada.", "Completado", c.VERDE),
            (ICONOS["nlp"], "Análisis IA y NLP", "Extracción de entidades, sentimiento, urgencia y palabras clave.", "96% confianza", c.MORADO),
            (ICONOS["clasificacion"], "Clasificación automática", "Asignación de categoría, prioridad y riesgo operativo.", "Prioridad alta", c.NARANJA),
            (ICONOS["derivacion"], "Derivación inteligente", "Selección del equipo técnico según carga, experiencia y SLA.", "NOC Nivel 2", c.AZUL),
            (ICONOS["validacion"], "Validación del operador", "Confirmación o ajuste de la sugerencia generada por IA.", "Pendiente", c.NARANJA),
            (ICONOS["tecnica"], "Atención técnica", "Resolución guiada por historial, conocimiento y contexto.", "En progreso", c.AZUL),
            (ICONOS["cierre"], "Cierre del ticket", "Validación final, satisfacción del usuario y aprendizaje del modelo.", "SLA OK", c.VERDE),
        ]

        for i, (icono, titulo, desc, badge, color) in enumerate(pasos):
            card = ctk.CTkFrame(scroll_horizontal, width=235, height=205, fg_color="#FFFFFF", corner_radius=18, border_width=1, border_color=c.BORDE)
            card.grid(row=0, column=i * 2, padx=8, pady=8)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=icono, font=fuente(32), text_color=color).pack(anchor="w", padx=16, pady=(16, 8))
            ctk.CTkLabel(card, text=titulo, font=fuente(14, "bold"), text_color=c.TEXTO, wraplength=190, justify="left").pack(anchor="w", padx=16)
            ctk.CTkLabel(card, text=desc, font=fuente(12), text_color=c.TEXTO_SUAVE, wraplength=190, justify="left").pack(anchor="w", padx=16, pady=(8, 12))
            etiqueta(card, badge, "#F8FAFC", color, 130).pack(anchor="w", padx=16)
            if i < len(pasos) - 1:
                ctk.CTkLabel(scroll_horizontal, text="→", font=fuente(30, "bold"), text_color=c.AZUL).grid(row=0, column=i * 2 + 1, padx=4)

        inferior = ctk.CTkFrame(cont, fg_color="transparent")
        inferior.grid(row=2, column=0, sticky="ew", pady=18)
        inferior.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_metricas(inferior, 0, "Métricas SLA", [("Crítico", "30 min", c.ROJO), ("Alto", "4 h", c.NARANJA), ("Medio", "12 h", c.AZUL), ("Bajo", "24 h", c.VERDE)])
        self.card_confianza(inferior, 1)
        self.card_keywords(inferior, 2)

        decisiones = crear_card(cont)
        decisiones.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        decisiones.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkLabel(decisiones, text="Reglas inteligentes de derivación", font=fuente(18, "bold"), text_color=c.TEXTO).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(18, 10))
        reglas = [
            ("Impacto negocio", "Servicios críticos elevan prioridad automáticamente."),
            ("Carga del equipo", "Deriva al grupo con mejor disponibilidad."),
            ("Historial técnico", "Compara incidentes similares cerrados."),
        ]
        for i, (t, d) in enumerate(reglas):
            block = ctk.CTkFrame(decisiones, fg_color="#F8FAFC", corner_radius=14)
            block.grid(row=1, column=i, sticky="ew", padx=14, pady=(6, 18))
            ctk.CTkLabel(block, text=t, font=fuente(14, "bold"), text_color=c.AZUL_OSCURO).pack(anchor="w", padx=14, pady=(12, 4))
            ctk.CTkLabel(block, text=d, font=fuente(12), text_color=c.TEXTO_SUAVE, wraplength=260, justify="left").pack(anchor="w", padx=14, pady=(0, 12))

    def card_metricas(self, master, col, titulo, datos):
        card = crear_card(master)
        card.grid(row=0, column=col, sticky="nsew", padx=8)
        ctk.CTkLabel(card, text=titulo, font=fuente(17, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=18, pady=(18, 10))
        for nombre, valor, color in datos:
            fila = ctk.CTkFrame(card, fg_color="transparent")
            fila.pack(fill="x", padx=18, pady=6)
            ctk.CTkLabel(fila, text=nombre, font=fuente(13), text_color=c.TEXTO).pack(side="left")
            ctk.CTkLabel(fila, text=valor, font=fuente(13, "bold"), text_color=color).pack(side="right")

    def card_confianza(self, master, col):
        card = crear_card(master)
        card.grid(row=0, column=col, sticky="nsew", padx=8)
        ctk.CTkLabel(card, text="Indicadores de confianza IA", font=fuente(17, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=18, pady=(18, 10))
        datos = [("NLP", 96, c.MORADO), ("Prioridad", 91, c.NARANJA), ("Derivación", 88, c.AZUL)]
        for nombre, valor, color in datos:
            ctk.CTkLabel(card, text=f"{nombre} · {valor}%", font=fuente(12, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=18, pady=(8, 2))
            bg = ctk.CTkFrame(card, height=10, fg_color="#EEF2F7", corner_radius=8)
            bg.pack(fill="x", padx=18)
            ctk.CTkFrame(bg, height=10, width=valor * 2.5, fg_color=color, corner_radius=8).place(x=0, y=0)

    def card_keywords(self, master, col):
        card = crear_card(master)
        card.grid(row=0, column=col, sticky="nsew", padx=8)
        ctk.CTkLabel(card, text="Etiquetas IA detectadas", font=fuente(17, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=18, pady=(18, 10))
        palabras = [("servidor", c.ROJO), ("facturación", c.NARANJA), ("bloqueo", c.ROJO), ("VPN", c.AZUL), ("acceso", c.VERDE), ("latencia", c.MORADO)]
        wrap = ctk.CTkFrame(card, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=18, pady=8)
        for i, (p, color) in enumerate(palabras):
            etiqueta(wrap, p, "#F8FAFC", color, 95).grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="w")

    def simular(self):
        messagebox.showinfo("Análisis IA", "Simulación completada:\n\nPrioridad sugerida: Alta\nConfianza IA: 92%\nEquipo sugerido: NOC Nivel 2\nSLA objetivo: 4 horas")
