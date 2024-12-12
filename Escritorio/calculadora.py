import customtkinter as ctk
from Recursos.recursos import procesos_activos, actualizar_lista_procesos 

def abrir_calculadora():
    global procesos_activos  # Accede a la lista global de procesos activos

    # Añadir "Calculadora" a la lista de procesos activos
    procesos_activos.append("Calculadora")
    try:
        actualizar_lista_procesos()  # Actualizar la visualización de procesos
    except ValueError:
        print("No se pudo actualizar el proceso")
    except Exception as e:
        print(f"Ocurrió un error con la calculadora: {e}")  

    # Crear una nueva ventana para la calculadora
    calculadora = ctk.CTkToplevel()
    calculadora.geometry("300x400")
    calculadora.title("Calculadora")
    calculadora.attributes("-topmost", True)
    calculadora.resizable(False, False)  # No permitir redimensionar la ventana

    # Entrada para mostrar los números y operaciones
    global entrada  # Para que sea accesible desde la función calcular()
    entrada = ctk.CTkEntry(calculadora, width=200)
    entrada.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    def agregar_a_entrada(simbolo):
        entrada.insert("end", simbolo)

    # Función de cálculo
    def calcular():
        try:
            resultado = eval(entrada.get())  # Realiza el cálculo
            entrada.delete(0, "end")  # Limpia la entrada
            entrada.insert("end", resultado)  # Muestra el resultado
        except Exception as e:
            entrada.delete(0, "end")
            entrada.insert("end", "Error")

    # Función para limpiar la entrada
    def limpiar():
        entrada.delete(0, "end")

    # Botones de la calculadora
    botones = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
        ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('-', 4, 3),
    ]

    for (texto, fila, columna) in botones:
        if texto == '=':
            boton = ctk.CTkButton(calculadora, text=texto, width=50, height=50 ,command=calcular)
        elif texto == 'C':  # Limpiar la entrada
            boton = ctk.CTkButton(calculadora, text=texto, width=50, height=50 ,command=limpiar)
        else:
            boton = ctk.CTkButton(calculadora, text=texto, width=50, height=50 ,command=lambda t=texto: agregar_a_entrada(t))
        
        boton.grid(row=fila, column=columna, padx=10, pady=10)

    # Al cerrar la calculadora, quitarla de la lista de procesos activos
    def on_close():
        try:
            actualizar_lista_procesos()  # Actualiza la lista de procesos al cerrar
        except ValueError:
            print("La calculadora no estaba en la lista de procesos activos.")
        except Exception as e:
            print(f"Ocurrió un error al cerrar la calculadora: {e}")
        finally:
            procesos_activos.remove("Calculadora")
            calculadora.destroy()


    # Configurar el evento de cierre de ventana
    calculadora.protocol("WM_DELETE_WINDOW", on_close)

    calculadora.mainloop()

