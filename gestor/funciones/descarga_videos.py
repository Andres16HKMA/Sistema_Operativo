import customtkinter as ctk
import yt_dlp as youtube_dl
from tkinter import messagebox
import os

# Función para descargar el video
def descargar_video(url, calidad, usuario):
    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida.")
        return

    # Ruta de la carpeta donde se guardarán los videos
    carpeta_videos = r"C:/Users/mateo/OneDrive/Documentos/Sistema Operativo/users/"+ usuario +"/videos"  # Ruta específica

    if not os.path.exists(carpeta_videos):
        os.makedirs(carpeta_videos)  # Crear la carpeta "videos" si no existe

    # Configuración de youtube-dl para descargar el video en la carpeta especificada
    ydl_opts = {
        'format': f'bestvideo[height<={calidad}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Preferir MP4
        'outtmpl': os.path.join(carpeta_videos, '%(title)s.%(ext)s'),  # Ruta donde se guarda el video
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Descargar el video
        messagebox.showinfo("Éxito", "Video descargado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Función que crea la ventana emergente para ingresar los datos del video
def ventana_descarga_video(usuario):
    ventana_video = ctk.CTkToplevel()
    ventana_video.title("Descargar Video")

    # Ingresar la URL del video
    url_label = ctk.CTkLabel(ventana_video, text="Ingresa la URL del video:")
    url_label.pack(padx=10, pady=10)

    url_entry = ctk.CTkEntry(ventana_video, width=300)
    url_entry.pack(padx=10, pady=10)

    # Seleccionar la calidad del video
    calidad_label = ctk.CTkLabel(ventana_video, text="Elige la calidad (1080, 720, 480):")
    calidad_label.pack(padx=10, pady=10)

    calidad_var = ctk.StringVar(value="1080")  # Valor por defecto
    calidad_menu = ctk.CTkOptionMenu(ventana_video, variable=calidad_var, values=["1080", "720", "480", "best"])
    calidad_menu.pack(padx=10, pady=10)

    # Función que se llama para descargar el video
    def descargar_video_action():
        url = url_entry.get()
        calidad = calidad_var.get()
        descargar_video(url, calidad, usuario)  # Llamar a la función de descarga de video
        ventana_video.destroy()  # Cerrar la ventana de descarga de video

    # Botón para iniciar la descarga del video
    boton_descargar_video = ctk.CTkButton(ventana_video, text="Descargar Video", command=descargar_video_action)
    boton_descargar_video.pack(padx=10, pady=10)

