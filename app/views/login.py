import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from app.controllers.auth_controller import AuthError, validar_credenciales
from app.database.conexion import probar_conexion
from app.utils import colores as c
from app.utils.assets import ruta_logo
from app.utils.estilos import fuente


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=c.FONDO)
        self.pack(fill="both", expand=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_panel_login()
        self.crear_panel_derecho()
        self._mostrar_estado_bd()

    def _cargar_logo(self, nombre="logo_blue.png", size=(70, 70)):
        try:
            return ctk.CTkImage(
                light_image=Image.open(ruta_logo(nombre)),
                dark_image=Image.open(ruta_logo(nombre)),
                size=size,
            )
        except Exception:
            return None

    def crear_panel_login(self):
        izquierda = ctk.CTkFrame(self, fg_color=c.FONDO, corner_radius=0)
        izquierda.grid(row=0, column=0, sticky="nsew")
        izquierda.grid_rowconfigure(0, weight=1)
        izquierda.grid_columnconfigure(0, weight=1)

        tarjeta = ctk.CTkFrame(
            izquierda,
            width=445,
            height=575,
            fg_color=c.BLANCO,
            corner_radius=24,
            border_width=1,
            border_color=c.BORDE,
        )
        tarjeta.grid(row=0, column=0, sticky="")
        tarjeta.pack_propagate(False)

        self.logo_login = self._cargar_logo("logo_blue.png", (74, 74))
        logo_box = ctk.CTkFrame(tarjeta, width=86, height=86, fg_color="#EEF2FF", corner_radius=22)
        logo_box.pack(pady=(32, 10))
        logo_box.pack_propagate(False)
        if self.logo_login:
            ctk.CTkLabel(logo_box, image=self.logo_login, text="").pack(expand=True)
        else:
            ctk.CTkLabel(logo_box, text="AI", font=fuente(28, "bold"), text_color=c.AZUL).pack(expand=True)

        titulo = ctk.CTkLabel(
            tarjeta,
            text="SmartPriority AI",
            font=fuente(29, "bold"),
            text_color=c.AZUL_OSCURO,
        )
        titulo.pack(pady=(0, 5))

        subtitulo = ctk.CTkLabel(
            tarjeta,
            text="Sistema Inteligente de Priorización de Tickets",
            font=fuente(13),
            text_color=c.TEXTO_SUAVE,
        )
        subtitulo.pack(pady=(0, 25))

        lbl_usuario = ctk.CTkLabel(
            tarjeta,
            text="Correo electrónico",
            font=fuente(13, "bold"),
            text_color="#374151",
        )
        lbl_usuario.pack(anchor="w", padx=44)

        self.entry_usuario = ctk.CTkEntry(
            tarjeta,
            width=350,
            height=45,
            placeholder_text="admin@empresa.com",
            corner_radius=11,
            border_color="#D1D5DB",
            fg_color="#FFFFFF",
            font=fuente(13),
        )
        self.entry_usuario.pack(pady=(6, 18))
        self.entry_usuario.insert(0, "admin@empresa.com")

        lbl_password = ctk.CTkLabel(
            tarjeta,
            text="Contraseña",
            font=fuente(13, "bold"),
            text_color="#374151",
        )
        lbl_password.pack(anchor="w", padx=44)

        self.entry_password = ctk.CTkEntry(
            tarjeta,
            width=350,
            height=45,
            placeholder_text="Ingrese su contraseña",
            show="●",
            corner_radius=11,
            border_color="#D1D5DB",
            fg_color="#FFFFFF",
            font=fuente(13),
        )
        self.entry_password.pack(pady=(6, 18))
        self.entry_password.insert(0, "123456")
        self.entry_password.bind("<Return>", lambda _e: self.iniciar_sesion())

        opciones = ctk.CTkFrame(tarjeta, fg_color="transparent")
        opciones.pack(fill="x", padx=47, pady=(0, 4))
        opciones.grid_columnconfigure(0, weight=1)
        opciones.grid_columnconfigure(1, weight=1)

        self.recordarme = ctk.CTkCheckBox(
            opciones,
            text="Recordarme",
            checkbox_width=18,
            checkbox_height=18,
            fg_color=c.AZUL,
            hover_color=c.AZUL,
            font=fuente(12),
            text_color=c.TEXTO,
        )
        self.recordarme.grid(row=0, column=0, sticky="w")

        recuperar = ctk.CTkLabel(
            opciones,
            text="¿Olvidaste tu contraseña?",
            font=fuente(12),
            text_color=c.AZUL,
            cursor="hand2",
        )
        recuperar.grid(row=0, column=1, sticky="e")
        recuperar.bind(
            "<Button-1>",
            lambda _e: messagebox.showinfo(
                "Recuperar contraseña",
                "Función disponible en la siguiente versión.",
            ),
        )

        boton_ingresar = ctk.CTkButton(
            tarjeta,
            text="Iniciar sesión",
            width=350,
            height=46,
            fg_color=c.AZUL,
            hover_color="#1D4ED8",
            corner_radius=11,
            font=fuente(14, "bold"),
            command=self.iniciar_sesion,
        )
        boton_ingresar.pack(pady=(28, 14))

        separador = ctk.CTkFrame(tarjeta, width=350, height=1, fg_color=c.BORDE)
        separador.pack(pady=(0, 13))

        acceso = ctk.CTkLabel(
            tarjeta,
            text="Usuario demo: admin@empresa.com  |  Clave: 123456",
            font=fuente(11),
            text_color=c.TEXTO_SUAVE,
        )
        acceso.pack()

        self.estado_bd = ctk.CTkLabel(
            tarjeta,
            text="Verificando conexión PostgreSQL...",
            font=fuente(11, "bold"),
            text_color=c.TEXTO_SUAVE,
        )
        self.estado_bd.pack(pady=(10, 0))

    def crear_panel_derecho(self):
        derecha = ctk.CTkFrame(self, fg_color=c.AZUL_OSCURO, corner_radius=0)
        derecha.grid(row=0, column=1, sticky="nsew")
        derecha.grid_columnconfigure(0, weight=1)
        derecha.grid_rowconfigure(0, weight=1)

        contenido = ctk.CTkFrame(derecha, fg_color="transparent")
        contenido.grid(row=0, column=0, sticky="nsew", padx=70, pady=70)
        contenido.grid_columnconfigure(0, weight=1)

        badge = ctk.CTkLabel(
            contenido,
            text="Plataforma empresarial · PostgreSQL + IA",
            fg_color="#12306F",
            text_color="#BFDBFE",
            corner_radius=18,
            height=34,
            font=fuente(12, "bold"),
        )
        badge.grid(row=0, column=0, sticky="w", pady=(10, 30))

        self.logo_panel = self._cargar_logo("logo_white.png", (120, 120))
        if self.logo_panel:
            ctk.CTkLabel(contenido, image=self.logo_panel, text="").grid(row=1, column=0, sticky="w", pady=(0, 15))
        else:
            ctk.CTkLabel(contenido, text="IA", font=fuente(80, "bold"), text_color="white").grid(row=1, column=0, sticky="w", pady=(0, 15))

        titulo = ctk.CTkLabel(
            contenido,
            text="Priorización inteligente\npara operaciones TI",
            font=fuente(36, "bold"),
            text_color="white",
            justify="left",
        )
        titulo.grid(row=2, column=0, sticky="w")

        descripcion = ctk.CTkLabel(
            contenido,
            text=(
                "Automatiza el registro, análisis NLP, clasificación, derivación, "
                "validación operativa y cierre de tickets con métricas SLA en tiempo real."
            ),
            font=fuente(16),
            text_color="#DCE7FF",
            justify="left",
            wraplength=530,
        )
        descripcion.grid(row=3, column=0, sticky="w", pady=(22, 30))

        puntos = [
            "Clasificación automática por prioridad",
            "Derivación inteligente al equipo correcto",
            "Indicadores de confianza IA y SLA",
            "Panel de actividad y analíticas ejecutivas",
        ]
        for i, texto in enumerate(puntos, start=4):
            fila = ctk.CTkLabel(
                contenido,
                text=f"✓  {texto}",
                font=fuente(15, "bold"),
                text_color="#EAF2FF",
            )
            fila.grid(row=i, column=0, sticky="w", pady=6)

    def _mostrar_estado_bd(self):
        ok, mensaje = probar_conexion()
        if ok:
            self.estado_bd.configure(text=f"● {mensaje}", text_color=c.VERDE)
        else:
            self.estado_bd.configure(text="● PostgreSQL no conectado", text_color=c.NARANJA)

    def iniciar_sesion(self):
        correo = self.entry_usuario.get().strip()
        contrasena = self.entry_password.get().strip()

        if not correo or not contrasena:
            messagebox.showwarning("Campos vacíos", "Ingrese correo electrónico y contraseña.")
            return

        try:
            usuario = validar_credenciales(correo, contrasena)
        except AuthError as error:
            messagebox.showerror("Error de conexión", str(error))
            return

        if usuario:
            messagebox.showinfo(
                "Bienvenido",
                f"Inicio de sesión correcto.\nUsuario: {usuario['nombre']} {usuario['apellido']}\nRol: {usuario['rol']}",
            )
            self.master.show_dashboard(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
