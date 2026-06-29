import customtkinter as ctk
from tkinter import messagebox

from app.database.conexion import conexion_bd
from app.utils import colores as c
from app.utils.estilos import crear_card, crear_boton_primario, fuente


class ConfiguracionView(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color=c.FONDO)
        self.usuario = usuario
        self.crear_vista()

    def crear_vista(self):
        cont = ctk.CTkScrollableFrame(self, fg_color=c.FONDO, corner_radius=0)
        cont.pack(fill="both", expand=True, padx=24, pady=22)
        cont.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(cont, text="Configuración", font=fuente(26, "bold"), text_color=c.TEXTO).grid(row=0, column=0, columnspan=2, sticky="w")
        ctk.CTkLabel(cont, text="Parámetros generales, reglas IA, SLA y preferencias de plataforma", font=fuente(14), text_color=c.TEXTO_SUAVE).grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 18))

        general = crear_card(cont)
        general.grid(row=2, column=0, sticky="nsew", padx=8, pady=8)
        ctk.CTkLabel(general, text="General", font=fuente(18, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 10))
        self.entry_empresa = self.campo(general, "Nombre de la empresa", "SmartPriority AI")
        self.entry_correo = self.campo(general, "Correo de soporte", "soporte@smartpriority.com")
        self.switch_notificaciones = self.switch(general, "Activar notificaciones en tiempo real", True)
        self.switch_alertas = self.switch(general, "Mostrar alertas SLA críticas", True)

        ia = crear_card(cont)
        ia.grid(row=2, column=1, sticky="nsew", padx=8, pady=8)
        ctk.CTkLabel(ia, text="Motor de inteligencia artificial", font=fuente(18, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 10))
        self.switch_clasificacion = self.switch(ia, "Clasificación automática", True)
        self.switch_derivacion = self.switch(ia, "Derivación inteligente", True)
        self.switch_aprendizaje = self.switch(ia, "Aprendizaje con tickets cerrados", True)
        ctk.CTkLabel(ia, text="Umbral mínimo de confianza IA", font=fuente(13, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(18, 6))
        self.slider = ctk.CTkSlider(ia, from_=50, to=99, number_of_steps=49, progress_color=c.MORADO, button_color=c.MORADO)
        self.slider.set(85)
        self.slider.pack(fill="x", padx=20, pady=(0, 6))
        self.valor_slider = ctk.CTkLabel(ia, text="85%", font=fuente(12, "bold"), text_color=c.MORADO)
        self.valor_slider.pack(anchor="e", padx=20)
        self.slider.configure(command=lambda v: self.valor_slider.configure(text=f"{int(v)}%"))

        sla = crear_card(cont)
        sla.grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=16)
        sla.grid_columnconfigure((0, 1, 2, 3), weight=1)
        ctk.CTkLabel(sla, text="Políticas SLA por prioridad", font=fuente(18, "bold"), text_color=c.TEXTO).grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(18, 8))
        self.sla_entries = {}
        datos = [("Crítica", "30", c.ROJO), ("Alta", "120", c.NARANJA), ("Media", "480", c.AZUL), ("Baja", "1440", c.VERDE)]
        for i, (prioridad, minutos, color) in enumerate(datos):
            card = ctk.CTkFrame(sla, fg_color="#F8FAFC", corner_radius=14)
            card.grid(row=1, column=i, sticky="ew", padx=12, pady=(10, 18))
            ctk.CTkLabel(card, text=prioridad, font=fuente(14, "bold"), text_color=color).pack(anchor="w", padx=14, pady=(14, 4))
            entry = ctk.CTkEntry(card, height=38, corner_radius=10)
            entry.insert(0, minutos)
            entry.pack(fill="x", padx=14, pady=(4, 4))
            ctk.CTkLabel(card, text="minutos", font=fuente(11), text_color=c.TEXTO_SUAVE).pack(anchor="w", padx=14, pady=(0, 14))
            self.sla_entries[prioridad] = entry

        acciones = ctk.CTkFrame(cont, fg_color="transparent")
        acciones.grid(row=4, column=0, columnspan=2, sticky="e", padx=8, pady=(0, 24))
        crear_boton_primario(acciones, "Guardar cambios", command=self.guardar, width=170).pack(side="right", padx=6)

    def campo(self, master, label, value):
        ctk.CTkLabel(master, text=label, font=fuente(13, "bold"), text_color=c.TEXTO).pack(anchor="w", padx=20, pady=(10, 5))
        entry = ctk.CTkEntry(master, height=40, corner_radius=11, border_color=c.BORDE)
        entry.insert(0, value)
        entry.pack(fill="x", padx=20, pady=(0, 8))
        return entry

    def switch(self, master, text, enabled=False):
        sw = ctk.CTkSwitch(master, text=text, font=fuente(13), text_color=c.TEXTO, progress_color=c.AZUL)
        sw.pack(anchor="w", padx=20, pady=9)
        if enabled:
            sw.select()
        return sw

    def guardar(self):
        try:
            with conexion_bd(commit=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO configuracion_sistema (nombre_configuracion, valor, descripcion)
                    VALUES ('nombre_sistema', %s, 'Nombre visible de la plataforma')
                    ON CONFLICT (nombre_configuracion)
                    DO UPDATE SET valor = EXCLUDED.valor, fecha_actualizacion = CURRENT_TIMESTAMP
                    """,
                    (self.entry_empresa.get().strip(),),
                )
                cursor.execute(
                    """
                    INSERT INTO configuracion_sistema (nombre_configuracion, valor, descripcion)
                    VALUES ('umbral_confianza_ia', %s, 'Porcentaje mínimo de confianza recomendado')
                    ON CONFLICT (nombre_configuracion)
                    DO UPDATE SET valor = EXCLUDED.valor, fecha_actualizacion = CURRENT_TIMESTAMP
                    """,
                    (str(int(self.slider.get())),),
                )
                for prioridad, entry in self.sla_entries.items():
                    cursor.execute(
                        """
                        UPDATE sla_configuracion
                        SET tiempo_minutos = %s
                        WHERE id_prioridad = (SELECT id_prioridad FROM prioridades WHERE nombre = %s)
                        """,
                        (int(entry.get()), prioridad),
                    )
            messagebox.showinfo("Configuración guardada", "Los cambios fueron guardados correctamente en PostgreSQL.")
        except Exception as error:
            messagebox.showerror("No se pudo guardar", f"Revisa PostgreSQL o los valores ingresados.\n\nDetalle: {error}")
