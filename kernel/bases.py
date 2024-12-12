import sqlite3
import os

def create_database(db_file):
    """Crea una base de datos SQLite si no existe.

    Args:
        db_file (str): Ruta al archivo de la base de datos.
    """

    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario TEXT PRIMARY KEY,
                contrasena TEXT,
                rol TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Base de datos '{db_file}' creada exitosamente.")
    else:
        print(f"La base de datos '{db_file}' ya existe.")

# Ruta completa al archivo de la base de datos
DB_PATH = "usuarios.db"

# Crear la base de datos si no existe
create_database(DB_PATH)