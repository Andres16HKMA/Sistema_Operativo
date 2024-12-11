import hashlib
import os
import customtkinter as ctk
import os

CREDENCIALES_PATH = "credenciales.txt"

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def guardar_credenciales(usuario, contrasena, rol):
    with open(CREDENCIALES_PATH, "a") as archivo:
        archivo.write(f"{usuario},{encriptar_contrasena(contrasena)},{rol}\n") 
        ruta_base = os.path.join("usuarios", usuario)  # En la carpeta de tu proyecto "Sistema Operativo"
        subcarpetas = ["Documentos", "Musica", "Descargas", "Imágenes"]

    try:
            # Crear la carpeta base del usuario
            os.makedirs(ruta_base, exist_ok=True)

            # Crear subcarpetas dentro de la carpeta del usuario
            for carpeta in subcarpetas:
                os.makedirs(os.path.join(ruta_base, carpeta), exist_ok=True)
            print("Credenciales guardadas con éxito.")
    except Exception as e:
        print(f"Error al crear carpetas para el usuario {usuario}: {e}")




def cargar_credenciales():
    credenciales = {}
    if os.path.exists(CREDENCIALES_PATH):
        with open(CREDENCIALES_PATH, "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                
                # Comprobar si la línea contiene 2 o 3 elementos
                if len(datos) == 2:
                    usuario, contrasena_hash = datos
                    rol = "usuario"  # Rol predeterminado si no está especificado
                elif len(datos) == 3:
                    usuario, contrasena_hash, rol = datos
                
                credenciales[usuario] = (contrasena_hash, rol)
    return credenciales


def verificar_credenciales(usuario, contrasena):
    credenciales = cargar_credenciales()
    contrasena_hash = encriptar_contrasena(contrasena)
    
    # Obtener la tupla (contrasena_hash_guardado, rol) o None si el usuario no existe
    credencial = credenciales.get(usuario)
    
    # Verificar si el usuario existe y la contraseña es correcta
    if credencial and credencial[0] == contrasena_hash:
        return True
    return False

def abrir_ventana_crear_usuario(parent):
    ventana_crear_usuario = ctk.CTkToplevel(parent)
    ventana_crear_usuario.title("Crear Nuevo Usuario")
    ventana_crear_usuario.geometry("400x400")
    
    ventana_crear_usuario.attributes('-topmost', True)

    etiqueta_usuario = ctk.CTkLabel(ventana_crear_usuario, text="Nombre de Usuario", font=("Arial", 16))
    etiqueta_usuario.pack(pady=10)

    entry_nuevo_usuario = ctk.CTkEntry(ventana_crear_usuario, placeholder_text="Nuevo Usuario")
    entry_nuevo_usuario.pack(pady=10)

    etiqueta_contrasena = ctk.CTkLabel(ventana_crear_usuario, text="Contraseña", font=("Arial", 16))
    etiqueta_contrasena.pack(pady=10)

    entry_nueva_contrasena = ctk.CTkEntry(ventana_crear_usuario, placeholder_text="Nueva Contraseña", show="*")
    entry_nueva_contrasena.pack(pady=10)

    etiqueta_rol = ctk.CTkLabel(ventana_crear_usuario, text="Rol", font=("Arial", 16))
    etiqueta_rol.pack(pady=10)

    combo_rol = ctk.CTkComboBox(ventana_crear_usuario, values=["Administrador", "Usuario"])
    combo_rol.pack(pady=10)

    etiqueta_resultado = ctk.CTkLabel(ventana_crear_usuario, text="")
    etiqueta_resultado.pack(pady=10)

    boton_guardar = ctk.CTkButton(
        ventana_crear_usuario, 
        text="Guardar Usuario", 
        command=lambda: guardar_usuario(entry_nuevo_usuario, entry_nueva_contrasena, combo_rol, etiqueta_resultado, ventana_crear_usuario)
    )
    boton_guardar.pack(pady=10)

    def guardar_usuario(entry_usuario, entry_contrasena, combo_rol, etiqueta_resultado, ventana_crear_usuario):
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        rol = combo_rol.get()

        if usuario and contrasena and rol:
            guardar_credenciales(usuario, contrasena, rol)
            etiqueta_resultado.configure(text="Usuario creado exitosamente.")
            ventana_crear_usuario.destroy()
        else:
            etiqueta_resultado.configure(text="Por favor ingrese un usuario, una contraseña y seleccione un rol.")
