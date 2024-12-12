import os
import fitz  # PyMuPDF para visualizar PDFs
import customtkinter as ctk
from tkinter import Listbox, messagebox, Canvas, Scrollbar, ttk
from PIL import Image, ImageTk  # Importar ImageTk para mostrar imágenes
from docx import Document  # Asegúrate de tener la biblioteca python-docx instalada
from fpdf import FPDF  # Asegúrate de tener la biblioteca fpdf instalada
import csv
from openpyxl import Workbook  # Asegúrate de tener la biblioteca openpyxl instalada
from Recursos.recursos import actualizar_lista_procesos, procesos_activos  # Asegúrate de tener esta función importada
import sqlite3
from gestor.funciones.edicion import abrir_txt  # Asegúrate de que esté correctamente importada

gestor_abierto = False
gestor = None  # Esta será la referencia de la ventana del gestor


def obtener_rol(usuario):
    """Obtiene el rol de un usuario a partir de la base de datos.

    Args:
        usuario (str): Nombre de usuario.

    Returns:
        str: Rol del usuario (por ejemplo, 'admin' o 'usuario'). Si el usuario no existe, devuelve None.
    """

    conn = sqlite3.connect('usuarios.db')  # Ajusta la ruta a tu base de datos
    cursor = conn.cursor()

    cursor.execute('SELECT rol FROM usuarios WHERE usuario = ?', (usuario,))
    resultado = cursor.fetchone()
    global rol_usuario
    rol_usuario = resultado[0]  # Almacena el rol en la variable global
    conn.close()
    return rol_usuario

# Función para mostrar el gestor de archivos
def mostrar_gestor_archivos(usuario):

    global gestor_abierto, gestor

    if gestor_abierto:
        print("El gestor ya está abierto.")
        return  # Si ya está abierto, no hacemos nada
    
    # Si no está abierto, creamos y mostramos la ventana del gestor
    gestor_abierto = True  # Marcamos que el gestor está abierto
    # Crear la carpeta base para el usuario
    ruta_base_usuario = "C:/Users/mateo/OneDrive/Documentos/Sistema Operativo/users/" + usuario  # Adjust the path as needed
    raiz = "C:/Users/mateo/OneDrive/Documentos/Sistema Operativo/users" # Adjust the path as needed

    # Crear la ventana del gestor
    global gestor  # Asegúrate de que el gestor se pueda referenciar en el cierre
    gestor = ctk.CTk()
    gestor.geometry("800x600")
    gestor.title(f"Gestor de Archivos - {usuario}")
    gestor.attributes("-topmost", True)

    gestor.resizable(False, False)  # No permitir redimensionar la ventana

    procesos_activos.append("Gestor de Archivos")  # Asegúrate de que procesos_activos esté definido
    try:
        actualizar_lista_procesos()  # Actualizar la visualización de procesos
    except ValueError:
        print("No se pudo actualizar el proceso")
    except Exception as e:
        print(f"Ocurrió un error con el gestor: {e}")      
    # Frame principal
    frame = ctk.CTkFrame(gestor, fg_color="#282c34")
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Función para listar archivos y carpetas dentro de la carpeta base del usuario

    def listar_archivos(ruta):
        rol_usuario = None  # Variable global para almacenar el rol del usuario

        if rol_usuario is None:
            rol_usuario = obtener_rol(usuario)

        if not ruta.startswith(ruta_base_usuario) and rol_usuario!="Administrador":  # Bloquea rutas fuera de la carpeta base
            messagebox.showerror("Error", "No tienes permiso para acceder a esta carpeta.")
            return

        lista_archivos.delete(0, ctk.END)  # Limpiar la lista
        try:
            archivos = os.listdir(ruta)
            for archivo in archivos:
                lista_archivos.insert(ctk.END, archivo)
        except PermissionError:
            messagebox.showerror("Error", "Permiso denegado en este directorio")

    # Función para abrir carpetas o archivos dentro de la carpeta base

    # Función para abrir PDFs y visualizarlos en una ventana
    def abrir_pdf(ruta_pdf):
        doc = fitz.open(ruta_pdf)
        ventana_pdf = ctk.CTkToplevel()
        ventana_pdf.title("Visor de PDF")
        ventana_pdf.geometry("800x600")

        canvas = Canvas(ventana_pdf)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(ventana_pdf, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        def mostrar_pagina(numero_pagina):
            if 0 <= numero_pagina < len(doc):
                page = doc[numero_pagina]
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagen_tk = ImageTk.PhotoImage(img)

                canvas.create_image(0, 0, anchor="nw", image=imagen_tk)
                canvas.image = imagen_tk
                canvas.config(scrollregion=canvas.bbox("all"))

        # Variables y funciones para cambiar de página
        pagina_actual = [0]  # Lista mutable para mantener referencia

        def siguiente_pagina():
            if pagina_actual[0] + 1 < len(doc):
                pagina_actual[0] += 1
                mostrar_pagina(pagina_actual[0])

        def pagina_anterior():
            if pagina_actual[0] > 0:
                pagina_actual[0] -= 1
                mostrar_pagina(pagina_actual[0])

        # Botones de navegación
        boton_atras = ctk.CTkButton(ventana_pdf, text="Anterior", command=pagina_anterior)
        boton_atras.pack(side="left", padx=5, pady=5)

        boton_siguiente = ctk.CTkButton(ventana_pdf, text="Siguiente", command=siguiente_pagina)
        boton_siguiente.pack(side="left", padx=5, pady=5)

        mostrar_pagina(pagina_actual[0])  # Mostrar la primera página al inicio

        
    # Función para abrir carpetas o archivos
    def abrir_item():
        seleccionado = lista_archivos.get(ctk.ACTIVE)  # lista_archivos está aquí en gestorArchivos.py
        nueva_ruta = os.path.join(entry_ruta.get(), seleccionado)
        
        if os.path.isdir(nueva_ruta):
            # Si es una carpeta, navegar dentro de ella
            entry_ruta.delete(0, ctk.END)
            entry_ruta.insert(0, nueva_ruta)
            listar_archivos(nueva_ruta)
        elif seleccionado.endswith(".txt"):
            # Pasar lista_archivos a la función abrir_txt
            abrir_txt(nueva_ruta, lista_archivos)
        elif seleccionado.endswith(".pdf"):
            abrir_pdf(nueva_ruta)
        else:
            messagebox.showinfo("Información", f"No se puede abrir el archivo '{seleccionado}'.")
    # Función para volver atrás en el directorio
    def volver_atras():
        if raiz!=entry_ruta.get():
            ruta_actual = entry_ruta.get()
            ruta_padre = os.path.dirname(ruta_actual)
            if ruta_padre.startswith(ruta_base_usuario) or rol_usuario=="Administrador":  # Solo permitir navegar dentro de la carpeta base
                entry_ruta.delete(0, ctk.END)
                entry_ruta.insert(0, ruta_padre)
                listar_archivos(ruta_padre)
            else:
                messagebox.showerror("Error", "No puedes salir de tu carpeta principal.")
        else:
            messagebox.showerror("Error", "No puede acceder mas atras.")
    def borrar_item():
        seleccionado = lista_archivos.get(ctk.ACTIVE)
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo o carpeta para eliminar.")
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar '{seleccionado}'?")
        if respuesta:
            ruta_a_borrar = os.path.join(entry_ruta.get(), seleccionado)
            try:
                if os.path.isfile(ruta_a_borrar):
                    os.remove(ruta_a_borrar)  # Borrar archivo
                else:
                    os.rmdir(ruta_a_borrar)  # Borrar carpeta (debe estar vacía)
                listar_archivos(entry_ruta.get())  # Actualizar la lista
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar '{seleccionado}': {e}")

 # Ruta actual
    entry_ruta = ctk.CTkEntry(frame, width=600)
    entry_ruta.grid(row=0, column=0, pady=10, padx=10)
    entry_ruta.insert(0, ruta_base_usuario)  # Configurar la ruta inicial a la carpeta del usuario

    # Botón para volver atrás
    boton_atras = ctk.CTkButton(frame, text="Atrás", command=volver_atras)
    boton_atras.grid(row=0, column=1, pady=10, padx=10)

    # Listbox para mostrar los archivos
    lista_archivos = Listbox(frame, height=20, width=80)
    lista_archivos.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
    listar_archivos(ruta_base_usuario)  # Listar archivos del directorio inicial

    # Botón para abrir el archivo o carpeta seleccionada
    boton_abrir = ctk.CTkButton(frame, text="Abrir", command=abrir_item)
    boton_abrir.grid(row=2, column=0, pady=10, padx=10)

    # Botón para borrar el archivo o carpeta seleccionada
    boton_borrar = ctk.CTkButton(frame, text="Borrar", command=borrar_item)
    boton_borrar.grid(row=2, column=1, pady=10, padx=10)


    # Función para crear un archivo desde el proyecto
    def crear_archivo():
    # Ventana emergente para pedir nombre del archivo
        ventana_archivo = ctk.CTkToplevel()
        ventana_archivo.title("Crear archivo")

        etiqueta = ctk.CTkLabel(ventana_archivo, text="Ingrese el nombre del archivo:")
        etiqueta.pack(padx=10, pady=10)

        entry_nombre_archivo = ctk.CTkEntry(ventana_archivo, width=300)
        entry_nombre_archivo.pack(padx=10, pady=10)

        # Crear una lista de tipos de archivo
        tipos_archivos = ["txt", "docx", "pdf", "csv", "xlsx", "jpg", "png"]

        # Combobox para seleccionar el tipo de archivo
        etiqueta_tipo = ctk.CTkLabel(ventana_archivo, text="Seleccione el tipo de archivo:")
        etiqueta_tipo.pack(padx=10, pady=10)

        combo_tipo_archivo = ttk.Combobox(ventana_archivo, values=tipos_archivos, state="readonly")
        combo_tipo_archivo.pack(padx=10, pady=10)
        combo_tipo_archivo.current(0)  # Seleccionar el primer tipo por defecto

        def confirmar_creacion():
            nombre_archivo = entry_nombre_archivo.get()
            tipo_archivo = combo_tipo_archivo.get()
            
            if nombre_archivo:
                nueva_ruta_archivo = os.path.join(entry_ruta.get(), f"{nombre_archivo}.{tipo_archivo}")

                # Crear el archivo de texto
                if tipo_archivo == "txt":
                    with open(nueva_ruta_archivo, 'w') as f:
                        f.write("Nuevo archivo creado")

                # Crear un archivo de Word (docx)
                elif tipo_archivo == "docx":
                    doc = Document()
                    doc.add_paragraph("Nuevo documento creado")
                    doc.save(nueva_ruta_archivo)

                # Crear un archivo PDF
                elif tipo_archivo == "pdf":
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt="Nuevo PDF creado", ln=True)
                    pdf.output(nueva_ruta_archivo)

                # Crear un archivo CSV
                elif tipo_archivo == "csv":
                    with open(nueva_ruta_archivo, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Nuevo", "archivo", "CSV", "creado"])

                # Crear un archivo Excel
                elif tipo_archivo == "xlsx":
                    wb = Workbook()
                    ws = wb.active
                    ws.append(["Nuevo archivo", "Excel", "creado"])
                    wb.save(nueva_ruta_archivo)

                # Para imágenes, simplemente creamos un archivo vacío
                elif tipo_archivo in ["jpg", "png"]:
                    with open(nueva_ruta_archivo, 'wb') as f:
                        f.write(b'')  # Crear un archivo vacío (no será una imagen válida)

                listar_archivos(entry_ruta.get())
                ventana_archivo.destroy()

        boton_confirmar = ctk.CTkButton(ventana_archivo, text="Crear", command=confirmar_creacion)
        boton_confirmar.pack(padx=10, pady=10)


    # Botón para crear un archivo nuevo
    boton_crear_archivo = ctk.CTkButton(frame, text="Crear Archivo", command=crear_archivo)
    boton_crear_archivo.grid(row=3, column=0, pady=10, padx=10)


    def on_close():
        try:
            actualizar_lista_procesos()  # Actualiza la lista de procesos al cerrar
        except ValueError:
            print("La gestor no estaba en la lista de procesos activos.")
        except Exception as e:
            print(f"Ocurrió un error al cerrar la gestor: {e}")
        finally:
            procesos_activos.remove("Gestor de Archivos")
            gestor.destroy()



    gestor.protocol("WM_DELETE_WINDOW", on_close)

    gestor.mainloop()
