import psutil
import customtkinter as ctk

# Lista global para almacenar los procesos activos
procesos_activos = []
label_procesos_text = None  # Inicialmente None

def actualizar_lista_procesos():
    global label_procesos_text  # Asegúrate de que sea global aquí
    if label_procesos_text and label_procesos_text.winfo_exists():  # Verificar si el widget sigue existiendo
        procesos_mostrados = "\n".join(procesos_activos) if procesos_activos else "No hay procesos activos."
        label_procesos_text.configure(text=f"Procesos Activos:\n{procesos_mostrados}")

def monitorear_recursos():
    global label_procesos_text  # Hacemos que la etiqueta sea global para actualizarla después

    # Crear una nueva ventana para mostrar los recursos
    ventana_recursos = ctk.CTk()
    ventana_recursos.geometry("600x400")
    ventana_recursos.title("Monitoreo de Recursos y Procesos")

    # Etiqueta estática para el título
    label_recursos = ctk.CTkLabel(ventana_recursos, text="Monitoreo de Recursos", font=("Arial", 16))
    label_recursos.pack(pady=10)

    # Etiqueta que actualizará el uso de memoria y CPU
    label_recursos_text = ctk.CTkLabel(ventana_recursos, text="", font=("Arial", 14))
    label_recursos_text.pack(pady=10)

    # Etiqueta para mostrar los procesos activos
    global label_procesos_text  # Ahora es global
    label_procesos_text = ctk.CTkLabel(ventana_recursos, text="Procesos Activos:", font=("Arial", 14))
    label_procesos_text.pack(pady=10)

    def actualizar_recursos():
        # Obtener información del uso de recursos del sistema principal
        proceso = psutil.Process()
        uso_cpu = proceso.cpu_percent(interval=1)
        memoria_info = proceso.memory_info()
        uso_memoria = memoria_info.rss / (1024 * 1024)

        # Actualizar el texto de uso de recursos
        label_recursos_text.configure(text=f"Uso de CPU: {uso_cpu}%\nUso de Memoria: {uso_memoria:.2f} MB")

        # Actualizar la lista de procesos
        actualizar_lista_procesos()

        # Repite el monitoreo cada 5 segundos
        if ventana_recursos.winfo_exists():  # Solo si la ventana sigue abierta
            ventana_recursos.after(5000, actualizar_recursos)

    actualizar_recursos()
    ventana_recursos.mainloop()

