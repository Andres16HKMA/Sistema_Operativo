import customtkinter as ctk
from PIL import Image
from Escritorio.calculadora import abrir_calculadora
from Recursos.recursos import monitorear_recursos
from Escritorio.gestorArchivos import mostrar_gestor_archivos  # Importar la función desde el archivo correcto
import time
def mostrar_escritorio():
    escritorio = ctk.CTk()
    escritorio.geometry("800x600")
    escritorio.title("Escritorio")
    escritorio.configure(fg_color="#56637e")  # Fondo gris oscuro

    frame = ctk.CTkFrame(escritorio, fg_color="#18252a")  # Cambiar color de fondo del frame
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    escritorio.grid_columnconfigure(0, weight=1)
    escritorio.grid_rowconfigure(0, weight=1)

    frame.grid_columnconfigure(0, weight=1)  # Izquierda (para el Omnitrix)
    frame.grid_rowconfigure(0, weight=1)  # Espacio superior
    frame.grid_rowconfigure(1, weight=1)  # Contenido (estrella y texto)
    frame.grid_rowconfigure(2, weight=1)  # Espacio inferior

    etiqueta_bienvenida = ctk.CTkLabel(frame, text="Bienvenido al Escritorio", font=("Arial", 24))
    etiqueta_bienvenida.grid(row=2, column=0, pady=10, padx=10)

    # Icono y botón de cerrar
    imagen_estrella = ctk.CTkImage(Image.open("imagenes/estrella.png"), size=(100, 100))
    boton_cerrar = ctk.CTkButton(frame, image=imagen_estrella, text="", fg_color="transparent", command=escritorio.destroy)
    boton_cerrar.grid(row=1, column=0, pady=10, padx=10)

    # Botón de Omnitrix
    imagen_omnitrix = ctk.CTkImage(Image.open("imagenes/omnitrix.png"), size=(100, 100))
    boton_omnitrix = ctk.CTkButton(frame, image=imagen_omnitrix, text="", fg_color="transparent", command=escritorio.destroy)
    boton_omnitrix.grid(row=4, column=0, padx=10, pady=10, sticky="sw")

    # Botón para abrir la calculadora
    imagen_calculadora = ctk.CTkImage(Image.open("imagenes/calculadora.png"), size=(100, 100))
    boton_calculadora = ctk.CTkButton(frame, image=imagen_calculadora, text="", fg_color="transparent", command=abrir_calculadora)
    boton_calculadora.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

    # Botón para abrir el monitor de recursos
    imagen_recursos = ctk.CTkImage(Image.open("imagenes/recursos.png"), size=(100, 100))
    boton_recursos = ctk.CTkButton(frame, image=imagen_recursos, text="", fg_color="transparent", command=monitorear_recursos)
    boton_recursos.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    # Botón para abrir el gestor de archivos
    imagen_gestor = ctk.CTkImage(Image.open("imagenes/gestor.png"), size=(100, 100))
    boton_gestor = ctk.CTkButton(frame, image=imagen_gestor, text="", fg_color="transparent", command=mostrar_gestor_archivos)
    boton_gestor.grid(row=0, column=0, padx=10, pady=10, sticky="sw")

    etiqueta_reloj = ctk.CTkLabel(frame, text="", font=("Arial", 14), fg_color="#18252a")
    etiqueta_reloj.grid(row=4, column=0, padx=10, pady=10, sticky="se")  # Ubicación en la esquina inferior derecha

    # Función para actualizar el reloj
    def actualizar_reloj():
        # Obtener la hora actual
        hora_actual = time.strftime("%H:%M:%S")
        fecha_actual = time.strftime("%Y-%m-%d")
        etiqueta_reloj.configure(text=f"{fecha_actual} {hora_actual}")  # Actualizar texto de la etiqueta
        etiqueta_reloj.after(1000, actualizar_reloj)  # Programar la próxima actualización en 1 segundo

    # Iniciar el reloj
    actualizar_reloj()
    escritorio.mainloop()