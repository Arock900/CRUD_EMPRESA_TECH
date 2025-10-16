#db.py

import sqlite3
import mysql.connector
from mysql.connector import Error
from config import Config


# ===============================
# 🔹 SECCIÓN SQLITE
# ===============================

def get_db():
    """Devuelve una conexión SQLite."""
    conn = sqlite3.connect("productos.db")
    return conn


def crear_tabla():
    """Crea la tabla 'productos' en SQLite si no existe."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("[OK] Tabla 'productos' (SQLite) creada o verificada correctamente ✅")

# ===============================
# 🔹 SECCIÓN MYSQL
# ===============================

def _build_connect_kwargs(include_db=True):
    """Prepara kwargs para mysql.connector.connect según config."""
    kwargs = {
        "host": getattr(Config, "MYSQL_HOST", "localhost"),
        "user": getattr(Config, "MYSQL_USER", "root"),
        "password": getattr(Config, "MYSQL_PASSWORD", ""),
        "port": getattr(Config, "MYSQL_PORT", 3306),
        "auth_plugin": getattr(Config, "MYSQL_AUTH_PLUGIN", None),  # opcional
    }
    # Eliminar valores None
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if include_db:
        kwargs["database"] = getattr(Config, "MYSQL_DB", None)

    return kwargs


def get_connection(use_db=True):
    """Devuelve una conexión MySQL usando la config centralizada."""
    kwargs = _build_connect_kwargs(include_db=use_db)
    return mysql.connector.connect(**kwargs)


def create_database_if_not_exists():
    """Crea la base de datos definida en Config.MYSQL_DB si no existe."""
    try:
        conn = get_connection(use_db=False)
        cursor = conn.cursor()
        db_name = getattr(Config, "MYSQL_DB", None)
        if not db_name:
            raise ValueError("Config.MYSQL_DB no está configurada.")

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "DEFAULT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';"
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[OK] Base de datos `{db_name}` asegurada/creada ✅")
    except Error as e:
        print("[ERROR] al crear la base de datos:", e)
        raise


def init_tables():
    """Crea las tablas básicas (productos y usuarios) si no existen en MySQL."""
    try:
        conn = get_connection(use_db=True)
        cursor = conn.cursor()

        # Tabla productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                categoria VARCHAR(100),
                precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                stock INT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Tabla `productos` (MySQL) asegurada/creada ✅")

        # Tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                usuario VARCHAR(50) UNIQUE NOT NULL,
                contrasena VARCHAR(255) NOT NULL,
                correo VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Tabla `usuarios` (MySQL) asegurada/creada ✅")

        conn.commit()
        cursor.close()
        conn.close()

    except Error as e:
        print("[ERROR] al crear tablas:", e)
        raise

def execute_query(sql, params=None, fetch=False):
    """
    Ejecuta una consulta SQL en MySQL.
    - Si fetch=True devuelve filas (lista de tuplas).
    - Siempre cierra la conexión.
    """
    try:
        conn = get_connection(use_db=True)
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        if fetch:
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return None
    except Error as e:
        print("[ERROR] execute_query:", e)
        raise

def obtener_usuario_por_nombre(usuario):
    """Devuelve un usuario (si existe) según su nombre de usuario."""
    sql = "SELECT * FROM usuarios WHERE usuario = %s"
    resultado = execute_query(sql, (usuario,), fetch=True)
    return resultado[0] if resultado else None


def registrar_usuario(nombre, usuario, contrasena, correo):
    """Registra un nuevo usuario en la base de datos."""
    sql = """
        INSERT INTO usuarios (nombre, usuario, contrasena, correo)
        VALUES (%s, %s, %s, %s)
    """
    execute_query(sql, (nombre, usuario, contrasena, correo))
    print(f"[OK] Usuario '{usuario}' registrado correctamente ✅")



def test_connection():
    """Prueba rápida: conecta y pide la versión del servidor MySQL."""
    try:
        conn = get_connection(use_db=True)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        print("[OK] Conexión exitosa. MySQL version:", version[0])
        return True
    except Error as e:
        print("[ERROR] test_connection:", e)
        return False


# ===============================
# 🔹 PUNTO DE ENTRADA
# ===============================

if __name__ == "__main__":
    print("== Iniciando comprobaciones de DB ==")
    create_database_if_not_exists()
    init_tables()
    ok = test_connection()
    if ok:
        print("== DB lista ✅ ==")
    else:
        print("== Hay un problema con la conexión ❌ ==")
