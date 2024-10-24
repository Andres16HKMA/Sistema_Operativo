import customtkinter as ctk
from PIL import Image
from Escritorio.escritorio import mostrar_escritorio
import hashlib
import os
import tkinter.font as tkFont  # Importar el módulo para manejar fuentes personalizadas

app = None  # Necesitamos que la app sea global para reiniciarla
CREDENCIALES_PATH = "credenciales.txt"

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def guardar_credenciales(usuario, contrasena):
    with open(CREDENCIALES_PATH, "w") as archivo:
        archivo.write(f"{usuario},{encriptar_contrasena(contrasena)}")
    print("Credenciales guardadas con éxito.")

def cargar_credenciales():
    if os.path.exists(CREDENCIALES_PATH):
        with open(CREDENCIALES_PATH, "r") as archivo:
            contenido = archivo.read().strip()
            if contenido:
                usuario, contrasena_hash = contenido.split(",")
                return usuario, contrasena_hash
    return None, None

def cerrar_interfaz(app):
    app.destroy()

def reiniciar_interfaz():
    global app  
    app.destroy()  
    iniciar_interfaz()  


# Función para iniciar sesión
def iniciar_sesion(entry_usuario, entry_contrasena, etiqueta_resultado, app):
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    usuario_guardado, contrasena_guardada_hash = cargar_credenciales()

    if usuario_guardado is None and contrasena_guardada_hash is None:
        # No hay credenciales guardadas, guardar las ingresadas
        guardar_credenciales(usuario, contrasena)
        etiqueta_resultado.configure(text="Usuario registrado exitosamente.")
    elif usuario == usuario_guardado and encriptar_contrasena(contrasena) == contrasena_guardada_hash:
        etiqueta_resultado.configure(text="Inicio de sesión exitoso.")
        app.destroy()  # Cierra la ventana de inicio de sesión
        mostrar_escritorio()  # Mostrar el escritorio
    else:
        etiqueta_resultado.configure(text="Usuario o contraseña incorrectos.")

# Función para iniciar la interfaz de inicio de sesión
def iniciar_interfaz():
    global app  
    app = ctk.CTk()
    app.geometry("800x400")
    app.title("Inicio de Sesión")

    # Crear un frame para el contenido principal
    frame = ctk.CTkFrame(app)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Establecer configuraciones de columna
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)
    frame.grid_columnconfigure(2, weight=1)


    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    

    # Cargar imágenes y mantener referencias
    frame.imagen_estrella = ctk.CTkImage(Image.open("imagenes/estrella.png"), size=(150, 150))
    boton_estrella = ctk.CTkButton(frame, image=frame.imagen_estrella, text="", fg_color="transparent", command=app.destroy)
    boton_estrella.grid(row=1, column=0, padx=10)

    frame.imagen_muneco = ctk.CTkImage(Image.open("imagenes/muñequito.png"), size=(150, 150))
    boton_muneco = ctk.CTkButton(frame, image=frame.imagen_muneco, text="", fg_color="transparent", command=reiniciar_interfaz)
    boton_muneco.grid(row=1, column=2, padx=10)

    titulo = ctk.CTkLabel(frame, text="gemOS", font=("Comic Sans MS", 32))
    titulo.grid(row=0, column=1, pady=10)

    entry_usuario = ctk.CTkEntry(frame, placeholder_text="Usuario", width=200)
    entry_usuario.grid(row=2, column=1, pady=10)

    entry_contrasena = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", width=200)
    entry_contrasena.grid(row=3, column=1, pady=10)

    etiqueta_resultado = ctk.CTkLabel(frame, text="")
    etiqueta_resultado.grid(row=5, column=1, pady=10)

    boton_iniciar_sesion = ctk.CTkButton(frame, text="Iniciar Sesión", command=lambda: iniciar_sesion(entry_usuario, entry_contrasena, etiqueta_resultado, app))
    boton_iniciar_sesion.grid(row=4, column=1, pady=10)

    app.mainloop()
