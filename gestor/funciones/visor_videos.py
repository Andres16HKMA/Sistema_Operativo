import os
import cv2
import tkinter as tk
import pygame
from tkinter import messagebox
from moviepy.editor import VideoFileClip

def abrir_video(archivo_video, usuario):
    if not archivo_video:
        messagebox.showerror("Error", "No se seleccionó un archivo de video válido.")
        return

    # Obtener la carpeta donde está el video
    carpeta_videos = r"C:/Users/mateo/OneDrive/Documentos/Sistema Operativo/users/" + usuario + "/videos"
    if not os.path.exists(carpeta_videos):
        messagebox.showerror("Error", "La carpeta de videos no existe.")
        return

    # Obtener el nombre del archivo de video sin la extensión
    nombre_video = os.path.splitext(os.path.basename(archivo_video))[0]

    # Crear la ruta del archivo de audio en la misma carpeta que el video
    archivo_audio = os.path.join(carpeta_videos, nombre_video + ".wav")

    # Crear una ventana para mostrar el video
    ventana_video = tk.Tk()
    ventana_video.title("Visualizador de Video")

    # Crear un objeto de captura de video con OpenCV
    cap = cv2.VideoCapture(archivo_video)

    if not cap.isOpened():
        messagebox.showerror("Error", "No se pudo abrir el archivo de video.")
        return

    # Obtener las dimensiones del primer cuadro del video
    ancho_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Crear un lienzo donde se mostrará el video
    lienzo = tk.Canvas(ventana_video, width=ancho_video, height=alto_video)
    lienzo.pack(fill="both", expand=True)

    # Usar moviepy para manejar tanto el video como el audio
    video_clip = VideoFileClip(archivo_video)
    audio_clip = video_clip.audio  # Extraer el audio del video

    # Guardar el audio extraído en la misma carpeta
    audio_clip.write_audiofile(archivo_audio)

    # Inicializar pygame para reproducir el audio
    pygame.mixer.init(frequency=audio_clip.fps)

    # Reproducir el audio con pygame
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()

    # Función para actualizar el video en el lienzo
    def actualizar_video():
        current_time = pygame.mixer.music.get_pos() / 1000  # Tiempo actual del audio (en segundos)
        
        # Asegurarse de que el video se reproduce en el tiempo adecuado
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)  # Establecer la posición actual del video según el tiempo del audio
        
        ret, frame = cap.read()
        if ret:
            # Redimensionar el frame al tamaño de la ventana
            frame_resized = cv2.resize(frame, (ventana_video.winfo_width(), ventana_video.winfo_height()))

            # Convertir la imagen a formato RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Convertir el frame a un formato que pueda ser mostrado en tkinter
            foto = tk.PhotoImage(master=lienzo, width=frame_rgb.shape[1], height=frame_rgb.shape[0], data=cv2.imencode('.png', frame_rgb)[1].tobytes())

            # Mostrar la imagen en el lienzo
            lienzo.create_image(0, 0, anchor=tk.NW, image=foto)
            lienzo.image = foto  # Mantener la referencia de la imagen

            # Acelerar la actualización del video para sincronizar con el audio
            lienzo.after(30, actualizar_video)  # Mantener la sincronización más precisa

        else:
            cap.release()  # Liberar los recursos cuando el video termine
            pygame.mixer.music.stop()  # Detener el audio cuando el video termine

    # Función para cerrar el video y detener el audio
    def cerrar_video():
        cap.release()  # Liberar los recursos
        pygame.mixer.music.stop()  # Detener el audio
        ventana_video.destroy()  # Cerrar la ventana del video

    # Asociar la función de cierre a la ventana
    ventana_video.protocol("WM_DELETE_WINDOW", cerrar_video)

    # Iniciar la reproducción del video
    actualizar_video()

    # Mostrar la ventana de video
    ventana_video.mainloop()
