from app.database.conexion import conexion_bd


class AuthError(Exception):
    """Error controlado de autenticación o conexión."""


def validar_credenciales(correo: str, contrasena: str):
    """Valida credenciales contra PostgreSQL.

    Devuelve un diccionario con los datos del usuario o None si las credenciales
    son incorrectas. Lanza AuthError si la base de datos no está disponible.
    """
    correo = correo.lower().strip()

    try:
        with conexion_bd() as cursor:
            cursor.execute(
                """
                SELECT
                    id_usuario,
                    nombre,
                    apellido,
                    correo,
                    rol,
                    estado
                FROM usuarios
                WHERE LOWER(correo) = %s
                  AND contrasena = %s
                  AND estado = TRUE
                LIMIT 1
                """,
                (correo, contrasena),
            )
            return cursor.fetchone()
    except Exception as error:
        raise AuthError(
            "No se pudo conectar con PostgreSQL. Revisa tu archivo .env, "
            "que la base smartpriority_ai exista y que el servicio PostgreSQL esté activo.\n\n"
            f"Detalle técnico: {error}"
        ) from error
