from Inicio.inicioSesion import iniciar_interfaz
from kernel.bases import create_database
import kernel.bases
import os
if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(kernel.bases.__file__), kernel.bases.DB_PATH)
    create_database(db_path)

    iniciar_interfaz() 
