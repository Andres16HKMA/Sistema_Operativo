import os
import customtkinter as ctk
from tkinter import messagebox, Text

# Modificar la definición de abrir_txt para que acepte 2 parámetros
def abrir_txt(ruta_txt, lista_archivos):
    # Crear una nueva ventana para el editor de texto
    ventana_editor = ctk.CTkToplevel()
    ventana_editor.title(f"Editor de Texto - {os.path.basename(ruta_txt)}")
    ventana_editor.geometry("600x500")

    # Área de texto para editar el archivo
    text_area = Text(ventana_editor, wrap="word", font=("Arial", 12))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    # Cargar el contenido del archivo .txt en el área de texto
    try:
        with open(ruta_txt, 'r', encoding='utf-8') as file:
            contenido = file.read()
            text_area.insert("1.0", contenido)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")
        ventana_editor.destroy()

    # Función para guardar los cambios
    def guardar_cambios():
        try:
            with open(ruta_txt, 'w', encoding='utf-8') as file:
                contenido_modificado = text_area.get("1.0", "end-1c")  # Obtener el texto desde el área de texto
                file.write(contenido_modificado)
            messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente.")
            ventana_editor.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    # Botón para guardar el archivo
    boton_guardar = ctk.CTkButton(ventana_editor, text="Guardar", command=guardar_cambios)
    boton_guardar.pack(padx=10, pady=10)

    # Función para cancelar y cerrar el editor
    def cancelar():
        ventana_editor.destroy()

    # Botón para cancelar y cerrar el editor
    boton_cancelar = ctk.CTkButton(ventana_editor, text="Cancelar", command=cancelar)
    boton_cancelar.pack(padx=10, pady=10)
