import tkinter as tk

# --- 1. Funciones Lógicas (Callbacks) ---
# Esta función se ejecutará SOLO cuando el usuario presione el botón
def accion_boton():
    # Cambiamos el texto de la etiqueta existente
    etiqueta_estado.config(text="¡Botón presionado!", fg="green")
    print("El alumno hizo clic en la interfaz") # Esto se ve en la consola de fondo

# --- 2. Creación de la Ventana Principal ---
ventana = tk.Tk()
ventana.title("Introducción a GUI")
ventana.geometry("300x200") # Definimos el tamaño: Ancho x Alto

# --- 3. Creación de Widgets (Elementos visuales) ---
# Creamos una etiqueta de texto y la asociamos a la 'ventana'
etiqueta_titulo = tk.Label(ventana, text="Laboratorio de Interfaces", font=("Arial", 14, "bold"))
# pack() "empaqueta" el widget en la ventana. pady agrega un margen vertical.
etiqueta_titulo.pack(pady=10)

# Creamos una segunda etiqueta que cambiará de estado luego
etiqueta_estado = tk.Label(ventana, text="Esperando acción...", font=("Arial", 12))
etiqueta_estado.pack(pady=10)

# Creamos el botón. El parámetro 'command' enlaza el clic con la función 'accion_boton'
# Nota importante para los alumnos: va sin paréntesis () al final del nombre de la función
boton_prueba = tk.Button(ventana, text="Haz clic aquí", command=accion_boton, bg="lightblue")
boton_prueba.pack(pady=10)

# --- 4. Bucle Principal de la Interfaz ---
# Esto mantiene la ventana abierta y escucha los clics del mouse o el teclado
ventana.mainloop()