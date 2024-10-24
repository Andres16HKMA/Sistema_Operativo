import psutil
import customtkinter as ctk

def monitorear_recursos():
    # Crear una nueva ventana para mostrar los recursos
    ventana_recursos = ctk.CTk()
    ventana_recursos.geometry("400x300")
    ventana_recursos.title("Monitoreo de Recursos")

    # Etiqueta estática para el título
    label_recursos = ctk.CTkLabel(ventana_recursos, text="Monitoreo de Recursos", font=("Arial", 16))
    label_recursos.pack(pady=10)

    # Etiqueta que actualizará el uso de memoria y CPU
    label_recursos_text = ctk.CTkLabel(ventana_recursos, text="", font=("Arial", 14))
    label_recursos_text.pack(pady=10)

    def actualizar_recursos():
        proceso = psutil.Process()
        uso_cpu = proceso.cpu_percent(interval=1)
        memoria_info = proceso.memory_info()
        uso_memoria = memoria_info.rss / (1024 * 1024)

        label_recursos_text.configure(text=f"Uso de CPU: {uso_cpu}%\nUso de Memoria: {uso_memoria:.2f} MB")
        ventana_recursos.after(5000, actualizar_recursos)  # Repite el monitoreo cada 5 segundos

    actualizar_recursos()
    ventana_recursos.mainloop()
