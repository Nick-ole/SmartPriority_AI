"""Modelo referencial de usuario.

La aplicación usa PostgreSQL como fuente principal. Este archivo solo documenta
la estructura esperada de un usuario dentro de la interfaz.
"""

USUARIO_DEMO = {
    "id_usuario": 1,
    "nombre": "Administrador",
    "apellido": "Sistema",
    "correo": "admin@empresa.com",
    "rol": "Administrador",
}
