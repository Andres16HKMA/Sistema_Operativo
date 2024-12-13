import os
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk

def abrir_visor_imagenes(ruta_imagen):
    # Crear la ventana principal del visor
    visor = Tk()
    visor.title("Visor de Imágenes")
    visor.geometry("800x600")  # Tamaño fijo
    visor.resizable(False, False)  # No permitir redimensionar

    # Etiqueta para mostrar la imagen
    etiqueta_imagen = Label(visor)
    etiqueta_imagen.pack(expand=True)

    # Variable para mantener la referencia de la imagen
    imagen_ref = {"imagen": None}

    def cargar_imagen(ruta):
        try:
            imagen = Image.open(ruta)
            # Usar LANCZOS para redimensionar la imagen
            imagen = imagen.resize((800, 600), Image.Resampling.LANCZOS)  
            imagen_tk = ImageTk.PhotoImage(imagen)
            etiqueta_imagen.configure(image=imagen_tk)
            imagen_ref["imagen"] = imagen_tk  # Mantener referencia
        except Exception as e:
            etiqueta_imagen.configure(text=f"Error al abrir la imagen: {e}", image=None)

    # Cargar la imagen inicial pasada como parámetro
    cargar_imagen(ruta_imagen)

    # Botón para cerrar el visor
    boton_cerrar = Button(visor, text="Cerrar", command=visor.destroy)
    boton_cerrar.pack(pady=10)

    # Iniciar el visor
    visor.mainloop()
