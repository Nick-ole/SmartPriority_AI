import customtkinter as ctk
from tkinter import messagebox

from app.controllers.ticket_controller import (
    TicketError,
    crear_ticket,
    listar_tickets,
    obtener_catalogos,
    previsualizar_analisis,
)
from app.utils import colores as c
from app.utils.estilos import crear_card, crear_boton_primario, crear_boton_secundario, fuente, etiqueta


class TicketsView(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color=c.FONDO)
        self.usuario = usuario or {}
        self.tickets = listar_tickets()
        self.crear_vista()

    def crear_vista(self):
        cont = ctk.CTkFrame(self, fg_color=c.FONDO)
        cont.pack(fill="both", expand=True, padx=28, pady=24)
        cont.grid_columnconfigure(0, weight=1)
        cont.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(cont, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Gestión de incidencias", font=fuente(26, "bold"), text_color=c.TEXTO).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Registro, búsqueda, clasificación IA y seguimiento de tickets desde PostgreSQL", font=fuente(14), text_color=c.TEXTO_SUAVE).grid(row=1, column=0, sticky="w", pady=(2, 0))
        crear_boton_secundario(header, "Actualizar", command=self.actualizar, width=110).grid(row=0, column=1, rowspan=2, padx=8)
        crear_boton_primario(header, "+ Nueva incidencia", command=self.nueva_incidencia, width=170).grid(row=0, column=2, rowspan=2)

        filtros = crear_card(cont)
        filtros.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        filtros.grid_columnconfigure(0, weight=1)
        self.buscar = ctk.CTkEntry(filtros, placeholder_text="Buscar por código, título, área, prioridad o equipo...", height=42, corner_radius=12, border_color=c.BORDE)
        self.buscar.grid(row=0, column=0, sticky="ew", padx=16, pady=16)
        self.buscar.bind("<KeyRelease>", lambda _e: self.render_tabla())
        self.filtro_prioridad = ctk.CTkComboBox(filtros, values=["Todas", "Crítica", "Alta", "Media", "Baja"], width=150, height=42, command=lambda _v: self.render_tabla())
        self.filtro_prioridad.set("Todas")
        self.filtro_prioridad.grid(row=0, column=1, padx=(0, 16), pady=16)

        self.tabla = crear_card(cont)
        self.tabla.grid(row=2, column=0, sticky="nsew")
        self.tabla.grid_columnconfigure(0, weight=1)
        self.render_tabla()

    def actualizar(self):
        self.tickets = listar_tickets()
        self.render_tabla()

    def tickets_filtrados(self):
        texto = self.buscar.get().lower().strip() if hasattr(self, "buscar") else ""
        prioridad = self.filtro_prioridad.get() if hasattr(self, "filtro_prioridad") else "Todas"
        resultado = []
        for ticket in self.tickets:
            coincide_texto = texto in " ".join(str(v).lower() for v in ticket.values())
            coincide_prioridad = prioridad == "Todas" or ticket["prioridad"] == prioridad
            if coincide_texto and coincide_prioridad:
                resultado.append(ticket)
        return resultado

    def render_tabla(self):
        for widget in self.tabla.winfo_children():
            widget.destroy()

        encabezado = ctk.CTkFrame(self.tabla, fg_color="#F8FAFC", corner_radius=12)
        encabezado.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 4))
        columnas = ["Código", "Incidencia", "Prioridad", "Estado", "SLA", "Confianza IA", "Equipo", "Acción"]
        pesos = [1, 4, 1, 1, 1, 1, 2, 1]
        for idx, peso in enumerate(pesos):
            encabezado.grid_columnconfigure(idx, weight=peso)
        for idx, col in enumerate(columnas):
            ctk.CTkLabel(encabezado, text=col, font=fuente(12, "bold"), text_color=c.TEXTO_SUAVE).grid(row=0, column=idx, sticky="w", padx=10, pady=10)

        filtrados = self.tickets_filtrados()
        if not filtrados:
            ctk.CTkLabel(
                self.tabla,
                text="No se encontraron tickets con los filtros seleccionados.",
                font=fuente(13),
                text_color=c.TEXTO_SUAVE,
            ).grid(row=1, column=0, pady=28)
            return

        for row, ticket in enumerate(filtrados, start=1):
            fila = ctk.CTkFrame(self.tabla, fg_color="white", corner_radius=12)
            fila.grid(row=row, column=0, sticky="ew", padx=14, pady=5)
            for idx, peso in enumerate(pesos):
                fila.grid_columnconfigure(idx, weight=peso)

            prioridad = ticket.get("prioridad", "Media")
            ctk.CTkLabel(fila, text=ticket["id"], font=fuente(12, "bold"), text_color=c.AZUL).grid(row=0, column=0, sticky="w", padx=10, pady=12)
            bloque = ctk.CTkFrame(fila, fg_color="transparent")
            bloque.grid(row=0, column=1, sticky="w", padx=10)
            ctk.CTkLabel(bloque, text=ticket["titulo"], font=fuente(12, "bold"), text_color=c.TEXTO, anchor="w", wraplength=350, justify="left").pack(anchor="w")
            ctk.CTkLabel(bloque, text=f"{ticket.get('categoria', '')} · {ticket.get('solicitante', '')}", font=fuente(11), text_color=c.TEXTO_SUAVE, anchor="w", wraplength=350).pack(anchor="w")

            etiqueta(fila, prioridad, c.PRIORIDAD_FONDO.get(prioridad, c.AZUL_CLARO), c.PRIORIDAD_COLOR.get(prioridad, c.AZUL), 78).grid(row=0, column=2, sticky="w", padx=10)
            ctk.CTkLabel(fila, text=ticket["estado"], font=fuente(12), text_color=c.TEXTO).grid(row=0, column=3, sticky="w", padx=10)
            sla_color = c.ROJO if ticket.get("sla") == "SLA vencido" else (c.NARANJA if prioridad in ["Crítica", "Alta"] else c.TEXTO_SUAVE)
            ctk.CTkLabel(fila, text=ticket["sla"], font=fuente(12, "bold"), text_color=sla_color).grid(row=0, column=4, sticky="w", padx=10)
            ctk.CTkLabel(fila, text=f'{float(ticket.get("confianza", 0)):.0f}%', font=fuente(12, "bold"), text_color=c.MORADO).grid(row=0, column=5, sticky="w", padx=10)
            ctk.CTkLabel(fila, text=ticket.get("equipo", "Sin asignar"), font=fuente(12), text_color=c.TEXTO, wraplength=160, justify="left").grid(row=0, column=6, sticky="w", padx=10)
            ctk.CTkButton(fila, text="Ver", width=58, height=30, corner_radius=10, fg_color="#EEF2FF", text_color=c.AZUL_OSCURO, hover_color="#E0E7FF", command=lambda t=ticket: self.ver_ticket(t)).grid(row=0, column=7, padx=10)

    def nueva_incidencia(self):
        win = ctk.CTkToplevel(self)
        win.title("Nueva incidencia")
        win.geometry("620x660")
        win.configure(fg_color=c.FONDO)
        win.grab_set()

        card = crear_card(win)
        card.pack(fill="both", expand=True, padx=22, pady=22)
        ctk.CTkLabel(card, text="Registrar incidencia", font=fuente(22, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=22, pady=(22, 6))
        ctk.CTkLabel(card, text="La IA analizará el texto, sugerirá prioridad, área, equipo y SLA.", font=fuente(13), text_color=c.TEXTO_SUAVE).pack(anchor="w", padx=22, pady=(0, 18))

        titulo = ctk.CTkEntry(card, placeholder_text="Título de la incidencia", height=42, corner_radius=12)
        titulo.pack(fill="x", padx=22, pady=8)

        catalogos = obtener_catalogos()
        areas = [a["nombre"] for a in catalogos.get("areas", [])]
        area = ctk.CTkComboBox(card, values=areas or ["Soporte Técnico"], height=42, corner_radius=12)
        area.set(areas[0] if areas else "Soporte Técnico")
        area.pack(fill="x", padx=22, pady=8)

        descripcion = ctk.CTkTextbox(card, height=145, corner_radius=12, border_width=1, border_color=c.BORDE)
        descripcion.pack(fill="x", padx=22, pady=8)
        descripcion.insert("1.0", "El servidor principal no responde y varios usuarios no pueden acceder al sistema.")

        resultado_card = ctk.CTkFrame(card, fg_color="#F8FAFC", corner_radius=14)
        resultado_card.pack(fill="x", padx=22, pady=(10, 4))
        self.lbl_resultado_ia = ctk.CTkLabel(
            resultado_card,
            text="Resultado IA: pendiente de análisis",
            font=fuente(13, "bold"),
            text_color=c.TEXTO_SUAVE,
            justify="left",
            wraplength=520,
        )
        self.lbl_resultado_ia.pack(anchor="w", padx=16, pady=14)

        def analizar():
            desc = descripcion.get("1.0", "end").strip()
            if not titulo.get().strip() or not desc:
                messagebox.showwarning("Falta información", "Ingrese título y descripción para analizar.")
                return None
            analisis = previsualizar_analisis(titulo.get(), desc)
            self.lbl_resultado_ia.configure(
                text=(
                    f"Prioridad sugerida: {analisis['prioridad']}  ·  "
                    f"Confianza: {analisis['confianza']:.1f}%\n"
                    f"Área sugerida: {analisis['area']}  ·  Equipo: {analisis['equipo']}\n"
                    f"SLA objetivo: {analisis['sla_minutos']} minutos\n"
                    f"Palabras clave: {analisis['palabras_clave']}"
                ),
                text_color=c.TEXTO,
            )
            return analisis

        def registrar():
            desc = descripcion.get("1.0", "end").strip()
            id_usuario = self.usuario.get("id_usuario", 1) if isinstance(self.usuario, dict) else 1
            try:
                resultado = crear_ticket(titulo.get(), desc, id_usuario=id_usuario, area_manual=area.get())
            except TicketError as error:
                messagebox.showerror("No se pudo registrar", str(error))
                return
            self.actualizar()
            win.destroy()
            messagebox.showinfo(
                "Incidencia registrada",
                f"Ticket {resultado['codigo']} registrado y analizado por IA.\n"
                f"Prioridad: {resultado['prioridad']}\n"
                f"Equipo sugerido: {resultado['equipo']}\n"
                f"Confianza: {resultado['confianza']:.1f}%",
            )

        acciones = ctk.CTkFrame(card, fg_color="transparent")
        acciones.pack(fill="x", padx=22, pady=20)
        crear_boton_secundario(acciones, "Analizar con IA", command=analizar, width=160).pack(side="left")
        crear_boton_primario(acciones, "Guardar ticket", command=registrar, width=170).pack(side="right")

    def ver_ticket(self, ticket):
        messagebox.showinfo(
            ticket["id"],
            f"Incidencia: {ticket['titulo']}\n"
            f"Solicitante: {ticket.get('solicitante', 'N/D')}\n"
            f"Área: {ticket.get('categoria', 'N/D')}\n"
            f"Prioridad: {ticket['prioridad']}\n"
            f"Estado: {ticket['estado']}\n"
            f"SLA: {ticket['sla']}\n"
            f"Confianza IA: {float(ticket.get('confianza', 0)):.1f}%\n"
            f"Equipo: {ticket.get('equipo', 'Sin asignar')}\n\n"
            f"Descripción:\n{ticket.get('descripcion', '')}",
        )
