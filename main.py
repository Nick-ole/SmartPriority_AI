import customtkinter as ctk
from tkinter import PhotoImage

from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.utils.assets import ruta_logo


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SmartPriorityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SmartPriority AI - Sistema Inteligente de Tickets")
        self.geometry("1366x768")
        self.minsize(1120, 700)
        self.usuario_actual = None
        self._vista = None
        self._configurar_icono()
        self.show_login()

    def _configurar_icono(self):
        try:
            self.icono_app = PhotoImage(file=ruta_logo("logo_blue.png"))
            self.iconphoto(True, self.icono_app)
        except Exception:
            pass

    def limpiar_vista(self):
        if self._vista is not None:
            self._vista.destroy()
            self._vista = None

    def show_login(self):
        self.usuario_actual = None
        self.limpiar_vista()
        self._vista = LoginView(self)

    def show_dashboard(self, usuario):
        self.usuario_actual = usuario
        self.limpiar_vista()
        self._vista = DashboardView(self, usuario=usuario)


if __name__ == "__main__":
    app = SmartPriorityApp()
    app.mainloop()
