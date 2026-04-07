import tkinter as tk
import serial
import time

# --- 1. Configuración del Puerto Serial ---
# IMPORTANTE: Recordar a los alumnos cambiar 'COM3' por su puerto asignado
try:
    puerto_serial = serial.Serial('COM3', 115200, timeout=1, dsrdtr=False)
    time.sleep(2) # Pausa necesaria para que la Pico inicialice correctamente
except serial.SerialException:
    print("Error: No se pudo abrir el puerto COM3. Revisa la conexión.")

# --- 2. Función Lógica (Callback Único) ---
def enviar_comando(instruccion):
    # Usamos f-strings para armar el comando y agregamos los saltos de línea
    comando = f"{instruccion}\r\n"
    # Codificamos a bytes (utf-8) y enviamos
    puerto_serial.write(comando.encode('utf-8'))
    print(f"Comando enviado: {instruccion}")

# --- 3. Función para cerrar todo de forma segura ---
def cerrar_aplicacion():
    if 'puerto_serial' in globals() and puerto_serial.is_open:
        puerto_serial.close() # Liberamos el puerto COM
    ventana.destroy()     # Cerramos la ventana

# --- 4. Creación de la Interfaz Gráfica ---
ventana = tk.Tk()
ventana.title("Control Serial Simple")
ventana.geometry("300x400") # Ventana un poco más alta para que quepan más botones

# Interceptar el botón "X" de la ventana para cerrar el puerto serial
ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Etiqueta de título
etiqueta = tk.Label(ventana, text="Control de Actuadores", font=("Arial", 12))
etiqueta.pack(pady=15)

# --- Botones usando lambda ---
# LED Rojo
boton_on_r = tk.Button(ventana, text="Rojo ON", command=lambda: enviar_comando("rojo on"), bg="red", fg="white", width=15)
boton_on_r.pack(pady=5)

boton_off_r = tk.Button(ventana, text="Rojo OFF", command=lambda: enviar_comando("rojo off"), bg="lightcoral", width=15)
boton_off_r.pack(pady=5)

# LED Verde (Ejemplo de cómo seguir agregando)
boton_on_v = tk.Button(ventana, text="Verde ON", command=lambda: enviar_comando("verde on"), bg="green", fg="white", width=15)
boton_on_v.pack(pady=5)

boton_off_v = tk.Button(ventana, text="Verde OFF", command=lambda: enviar_comando("verde off"), bg="lightgreen", width=15)
boton_off_v.pack(pady=5)

# Iniciamos el bucle de la interfaz
ventana.mainloop()