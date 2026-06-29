import customtkinter as ctk

from app.controllers.reporte_controller import (
    actividad_por_dia,
    obtener_kpis,
    rendimiento_equipos,
    tickets_por_categoria,
)
from app.utils import colores as c
from app.utils.estilos import crear_card, fuente


class ReportesView(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color=c.FONDO)
        self.usuario = usuario
        self.crear_vista()

    def crear_vista(self):
        cont = ctk.CTkScrollableFrame(self, fg_color=c.FONDO, corner_radius=0)
        cont.pack(fill="both", expand=True, padx=24, pady=22)
        cont.grid_columnconfigure((0, 1), weight=1)

        header = ctk.CTkFrame(cont, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Reportes y analíticas", font=fuente(26, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Monitoreo ejecutivo de rendimiento, SLA, volumen y confianza IA", font=fuente(14), text_color=c.TEXTO_SUAVE).grid(row=1, column=0, sticky="w")
        periodo = ctk.CTkComboBox(header, values=["Últimos 7 días", "Últimos 30 días", "Este trimestre"], width=160, height=38)
        periodo.set("Últimos 7 días")
        periodo.grid(row=0, column=1, rowspan=2, padx=8)

        for i, (nombre, valor, cambio, icono) in enumerate(obtener_kpis()):
            card = crear_card(cont)
            card.grid(row=1 + i // 2, column=i % 2, sticky="nsew", padx=8, pady=8)
            ctk.CTkLabel(card, text=f"{icono}  {nombre}", font=fuente(14, "bold"), text_color=c.TEXTO_SUAVE).pack(anchor="w", padx=18, pady=(16, 4))
            ctk.CTkLabel(card, text=valor, font=fuente(30, "bold"), text_color=c.AZUL_OSCURO).pack(anchor="w", padx=18)
            ctk.CTkLabel(card, text=cambio, font=fuente(12, "bold"), text_color=c.VERDE).pack(anchor="w", padx=18, pady=(0, 14))

        barras = crear_card(cont)
        barras.grid(row=3, column=0, sticky="nsew", padx=8, pady=16)
        ctk.CTkLabel(barras, text="Tickets por día", font=fuente(18, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 12))
        self.grafico_barras(barras, actividad_por_dia())

        cats = crear_card(cont)
        cats.grid(row=3, column=1, sticky="nsew", padx=8, pady=16)
        ctk.CTkLabel(cats, text="Distribución por área", font=fuente(18, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 12))
        self.grafico_horizontal(cats, tickets_por_categoria())

        tabla = crear_card(cont)
        tabla.grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 22))
        ctk.CTkLabel(tabla, text="Rendimiento por equipo", font=fuente(18, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 10))
        self.tabla_equipos(tabla)

    def grafico_barras(self, master, datos):
        if not datos:
            datos = [("Sin datos", 1)]
        max_val = max(v for _, v in datos) or 1
        chart = ctk.CTkFrame(master, fg_color="transparent", height=220)
        chart.pack(fill="x", padx=20, pady=(0, 20))
        chart.grid_columnconfigure(tuple(range(len(datos))), weight=1)
        for i, (dia, valor) in enumerate(datos):
            col = ctk.CTkFrame(chart, fg_color="transparent")
            col.grid(row=0, column=i, sticky="s", padx=6)
            altura = max(18, int((valor / max_val) * 150))
            ctk.CTkLabel(col, text=str(valor), font=fuente(11, "bold"), text_color=c.TEXTO_SUAVE).pack()
            ctk.CTkFrame(col, width=34, height=altura, fg_color=c.AZUL, corner_radius=10).pack(side="bottom")
            ctk.CTkLabel(col, text=dia, font=fuente(12), text_color=c.TEXTO_SUAVE).pack(pady=(8, 0))

    def grafico_horizontal(self, master, datos):
        if not datos:
            datos = [("Sin datos", 1)]
        max_val = max(v for _, v in datos) or 1
        for nombre, valor in datos:
            fila = ctk.CTkFrame(master, fg_color="transparent")
            fila.pack(fill="x", padx=20, pady=9)
            fila.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(fila, text=nombre, width=130, anchor="w", font=fuente(12, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w")
            bg = ctk.CTkFrame(fila, height=13, fg_color="#EEF2F7", corner_radius=8)
            bg.grid(row=0, column=1, sticky="ew", padx=10)
            ctk.CTkFrame(bg, height=13, width=max(35, int((valor / max_val) * 220)), fg_color=c.MORADO, corner_radius=8).place(x=0, y=0)
            ctk.CTkLabel(fila, text=str(valor), width=42, font=fuente(12, "bold"), text_color=c.TEXTO_SUAVE).grid(row=0, column=2)

    def tabla_equipos(self, master):
        encabezado = ctk.CTkFrame(master, fg_color="#F8FAFC", corner_radius=12)
        encabezado.pack(fill="x", padx=18, pady=(0, 6))
        for i, col in enumerate(["Equipo", "Confianza", "Carga", "Resueltos"]):
            encabezado.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(encabezado, text=col, font=fuente(12, "bold"), text_color=c.TEXTO_SUAVE).grid(row=0, column=i, sticky="w", padx=14, pady=10)
        for equipo, sla, tiempo, tickets in rendimiento_equipos():
            fila = ctk.CTkFrame(master, fg_color="white", corner_radius=12)
            fila.pack(fill="x", padx=18, pady=5)
            for i in range(4):
                fila.grid_columnconfigure(i, weight=1)
            valores = [equipo, sla, tiempo, tickets]
            for i, val in enumerate(valores):
                ctk.CTkLabel(fila, text=val, font=fuente(12, "bold" if i == 0 else "normal"), text_color=c.TEXTO if i == 0 else c.TEXTO_SUAVE).grid(row=0, column=i, sticky="w", padx=14, pady=12)
