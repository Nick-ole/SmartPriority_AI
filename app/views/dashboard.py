import customtkinter as ctk
from PIL import Image

from app.utils import colores as c
from app.utils.assets import ruta_logo
from app.utils.estilos import fuente
from app.utils.iconos import ICONOS
from app.views.panel_principal import PanelPrincipalView
from app.views.tickets import TicketsView
from app.views.flujo_ia import FlujoIAView
from app.views.reportes import ReportesView
from app.views.configuracion import ConfiguracionView


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master, fg_color=c.FONDO)
        self.usuario = usuario
        self.pack(fill="both", expand=True)
        self.botones = {}
        self.vista_actual = None
        self.logo_sidebar = self._cargar_logo("logo_white.png", (38, 38))

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()
        self.crear_contenedor()
        self.mostrar_vista("Panel principal")

    def _cargar_logo(self, nombre, size):
        try:
            return ctk.CTkImage(
                light_image=Image.open(ruta_logo(nombre)),
                dark_image=Image.open(ruta_logo(nombre)),
                size=size,
            )
        except Exception:
            return None

    def nombre_usuario(self):
        if isinstance(self.usuario, dict):
            return f"{self.usuario.get('nombre', '')} {self.usuario.get('apellido', '')}".strip()
        return str(self.usuario)

    def correo_usuario(self):
        if isinstance(self.usuario, dict):
            return self.usuario.get("correo", "")
        return str(self.usuario)

    def rol_usuario(self):
        if isinstance(self.usuario, dict):
            return self.usuario.get("rol", "Operador")
        return "Operador"

    def crear_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=275, fg_color=c.AZUL_OSCURO, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(9, weight=1)

        logo = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo.grid(row=0, column=0, sticky="ew", padx=18, pady=(22, 28))

        logo_box = ctk.CTkFrame(logo, width=54, height=54, fg_color=c.AZUL, corner_radius=16)
        logo_box.pack(side="left")
        logo_box.pack_propagate(False)
        if self.logo_sidebar:
            ctk.CTkLabel(logo_box, image=self.logo_sidebar, text="").pack(expand=True)
        else:
            ctk.CTkLabel(logo_box, text="AI", font=fuente(18, "bold"), text_color="white").pack(expand=True)

        texto_logo = ctk.CTkFrame(logo, fg_color="transparent")
        texto_logo.pack(side="left", padx=12)
        ctk.CTkLabel(texto_logo, text="SmartPriority", font=fuente(20, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(texto_logo, text="AI Tickets", font=fuente(12), text_color="#BFDBFE").pack(anchor="w")

        opciones = [
            ("Panel principal", ICONOS["dashboard"]),
            ("Gestión de incidencias", ICONOS["tickets"]),
            ("Flujo inteligente IA", ICONOS["flujo"]),
            ("Reportes", ICONOS["reportes"]),
            ("Configuración", ICONOS["config"]),
        ]
        for i, (nombre, icono) in enumerate(opciones, start=1):
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icono}  {nombre}",
                height=44,
                corner_radius=12,
                anchor="w",
                fg_color="transparent",
                hover_color="#12306F",
                text_color="#DCE7FF",
                font=fuente(13, "bold"),
                command=lambda n=nombre: self.mostrar_vista(n),
            )
            btn.grid(row=i, column=0, sticky="ew", padx=14, pady=4)
            self.botones[nombre] = btn

        usuario_card = ctk.CTkFrame(sidebar, fg_color="#102B66", corner_radius=16)
        usuario_card.grid(row=10, column=0, sticky="ew", padx=14, pady=(10, 12))
        ctk.CTkLabel(usuario_card, text=self.rol_usuario(), font=fuente(12, "bold"), text_color="#BFDBFE").pack(anchor="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(usuario_card, text=self.nombre_usuario(), font=fuente(13, "bold"), text_color="white", wraplength=220, justify="left").pack(anchor="w", padx=14)
        ctk.CTkLabel(usuario_card, text=self.correo_usuario(), font=fuente(11), text_color="#DCE7FF", wraplength=220, justify="left").pack(anchor="w", padx=14, pady=(0, 12))

        salir = ctk.CTkButton(
            sidebar,
            text=f"{ICONOS['salir']}  Cerrar sesión",
            height=42,
            corner_radius=12,
            anchor="w",
            fg_color="#12306F",
            hover_color="#1E3A8A",
            text_color="white",
            font=fuente(13, "bold"),
            command=self.master.show_login,
        )
        salir.grid(row=11, column=0, sticky="ew", padx=14, pady=(0, 18))

    def crear_contenedor(self):
        main = ctk.CTkFrame(self, fg_color=c.FONDO, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        topbar = ctk.CTkFrame(main, height=72, fg_color=c.BLANCO, corner_radius=0)
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=0)
        topbar.grid_columnconfigure(2, weight=0)

        self.titulo_topbar = ctk.CTkLabel(topbar, text="Panel principal", font=fuente(20, "bold"), text_color=c.AZUL_OSCURO)
        self.titulo_topbar.grid(row=0, column=0, sticky="w", padx=24)

        buscador = ctk.CTkEntry(topbar, placeholder_text="Buscar ticket, usuario o reporte...", width=285, height=38, corner_radius=12, border_color=c.BORDE)
        buscador.grid(row=0, column=1, sticky="e", padx=(0, 14))

        estado = ctk.CTkLabel(topbar, text="● Sistema operativo · IA activa", font=fuente(12, "bold"), text_color=c.VERDE)
        estado.grid(row=0, column=2, sticky="e", padx=(0, 24))

        self.contenido = ctk.CTkFrame(main, fg_color=c.FONDO, corner_radius=0)
        self.contenido.grid(row=1, column=0, sticky="nsew")
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)

    def mostrar_vista(self, nombre):
        for opcion, boton in self.botones.items():
            if opcion == nombre:
                boton.configure(fg_color=c.AZUL, text_color="white")
            else:
                boton.configure(fg_color="transparent", text_color="#DCE7FF")

        if self.vista_actual is not None:
            self.vista_actual.destroy()

        mapa = {
            "Panel principal": lambda parent: PanelPrincipalView(parent, usuario=self.usuario),
            "Gestión de incidencias": lambda parent: TicketsView(parent, usuario=self.usuario),
            "Flujo inteligente IA": lambda parent: FlujoIAView(parent, usuario=self.usuario),
            "Reportes": lambda parent: ReportesView(parent, usuario=self.usuario),
            "Configuración": lambda parent: ConfiguracionView(parent, usuario=self.usuario),
        }
        self.titulo_topbar.configure(text=nombre)
        self.vista_actual = mapa[nombre](self.contenido)
        self.vista_actual.grid(row=0, column=0, sticky="nsew")
