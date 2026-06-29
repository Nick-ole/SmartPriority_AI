"""Conexión centralizada a PostgreSQL para SmartPriority AI."""
import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    """Abre una conexión a PostgreSQL usando las variables del archivo .env."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "smartpriority_ai"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        cursor_factory=RealDictCursor,
    )


@contextmanager
def conexion_bd(commit: bool = False):
    """Context manager para consultas seguras.

    Uso:
        with conexion_bd() as cursor:
            cursor.execute("SELECT 1")
    """
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        yield cursor
        if commit:
            conexion.commit()
    except Exception:
        if conexion and commit:
            conexion.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def probar_conexion() -> tuple[bool, str]:
    try:
        with conexion_bd() as cursor:
            cursor.execute("SELECT current_database() AS db")
            resultado = cursor.fetchone()
        return True, f"Conectado a {resultado['db']}"
    except Exception as error:
        return False, str(error)
