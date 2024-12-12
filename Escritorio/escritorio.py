import customtkinter as ctk
from PIL import Image
from Escritorio.calculadora import abrir_calculadora
from Recursos.recursos import monitorear_recursos
from gestor.gestorArchivos import mostrar_gestor_archivos
from juegos.culebrita import iniciar_culebrita
import time
import requests  # Para acceder a la API del clima
import webview


# Clave y configuración de la API del clima
API_KEY = "663e66b760396f9d2f0198dd1483e3e0"
CIUDAD = "Manizales,CO"
URL_CLIMA = f"http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es"

def obtener_clima():
    try:
        respuesta = requests.get(URL_CLIMA)
        datos = respuesta.json()
        if respuesta.status_code == 200:
            temperatura = datos["main"]["temp"]
            descripcion = datos["weather"][0]["description"].capitalize()
            return f"{temperatura}°C, {descripcion}"
        else:
            return "Error al obtener el clima"
    except Exception as e:
        return "Sin conexión"

def mostrar_escritorio(usuario):  # Recibe el nombre del usuario como argumento
    escritorio = ctk.CTk()
    escritorio.geometry("1000x700")
    escritorio.title("Escritorio")
    escritorio.configure(fg_color="#56637e")  # Fondo gris oscuro
    escritorio.resizable(False, False)  # No permitir redimensionar la ventana

    frame = ctk.CTkFrame(escritorio, fg_color="#18252a")  # Cambiar color de fondo del frame
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    escritorio.grid_columnconfigure(0, weight=1)
    escritorio.grid_rowconfigure(0, weight=1)

    frame.grid_columnconfigure(0, weight=1)  # Izquierda (para el Omnitrix)
    frame.grid_rowconfigure(0, weight=1)  # Espacio superior
    frame.grid_rowconfigure(1, weight=1)  # Contenido (estrella y texto)
    frame.grid_rowconfigure(2, weight=1)  # Espacio inferior


    def iniciar_webview():
        webview.create_window('Mi Navegador Integrado', 'https://www.google.com')
        webview.start()

    etiqueta_bienvenida = ctk.CTkLabel(frame, text=f"Bienvenido, {usuario}", font=("Arial", 24))
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
    boton_gestor = ctk.CTkButton(frame, image=imagen_gestor, text="", fg_color="transparent", command=lambda: mostrar_gestor_archivos(usuario))
    boton_gestor.grid(row=0, column=0, padx=10, pady=10, sticky="sw")

    # Botón para abrir el juego de la culebrita
    imagen_culebrita = ctk.CTkImage(Image.open("imagenes/culebrita.png"), size=(100, 100))
    boton_culebrita = ctk.CTkButton(frame, image=imagen_culebrita, text="", fg_color="transparent", command=iniciar_culebrita)
    boton_culebrita.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    etiqueta_reloj = ctk.CTkLabel(frame, text="", font=("Arial", 14), fg_color="#18252a")
    etiqueta_reloj.grid(row=0, column=0, padx=10, pady=10, sticky="ne")  # Ubicación en la esquina inferior derecha
    
    etiqueta_clima = ctk.CTkLabel(frame, text="Cargando clima...", font=("Arial", 14), fg_color="#18252a")
    etiqueta_clima.grid(row=4, column=0, padx=10, pady=10, sticky="se")  # Justo arriba del reloj

    imagen_edge = ctk.CTkImage(Image.open("imagenes/edge.png"), size=(100, 100))
    boton_edge = ctk.CTkButton(frame, image=imagen_edge, text="", fg_color="transparent", command=iniciar_webview)

    boton_edge.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

    # Función para actualizar el reloj
    def actualizar_reloj_y_clima():
        # Actualizar la hora
        hora_actual = time.strftime("%H:%M:%S")
        fecha_actual = time.strftime("%Y-%m-%d")
        etiqueta_reloj.configure(text=f"{fecha_actual} {hora_actual}")
        
        # Actualizar el clima cada minuto
        if int(time.time()) % 60 == 0:  # Actualiza cada minuto
            etiqueta_clima.configure(text=obtener_clima())
        
        etiqueta_reloj.after(1000, actualizar_reloj_y_clima)  # Programar la próxima actualización en 1 segundo

    # Iniciar el reloj y clima
    etiqueta_clima.configure(text=obtener_clima())  # Mostrar clima inicial
    actualizar_reloj_y_clima()



    escritorio.mainloop()
