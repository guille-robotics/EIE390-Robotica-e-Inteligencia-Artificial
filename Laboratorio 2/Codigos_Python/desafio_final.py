import tkinter as tk
import serial
import time

# --- 1. Configuración del Puerto Serial ---
# IMPORTANTE: Recordar a los alumnos cambiar 'COM3' por su puerto asignado
puerto_serial = serial.Serial('COM3', 115200, timeout=1, dsrdtr=False)
time.sleep(2) # Pausa necesaria para que la Pico inicialice correctamente

# --- 2. Función Lógica (Callback) ---
def enviar_encendido():
    # Enviamos el comando "on" asegurando el salto de línea y codificando a bytes
    comando = "on\r\n"
    puerto_serial.write(comando.encode())
    print("Comando enviado: on")

def enviar_apagado():
    # Enviamos el comando "off" asegurando el salto de línea y codificando a bytes
    comando = "off\r\n"
    puerto_serial.write(comando.encode())
    print("Comando enviado: off")

def enviar_titilar():
    # Enviamos el comando "titilar" asegurando el salto de línea y codificando a bytes
    comando = "titilar\r\n"
    puerto_serial.write(comando.encode())
    print("Comando enviado: titilar")

# --- 3. Función para cerrar todo de forma segura ---
def cerrar_aplicacion():
    puerto_serial.close() # Liberamos el puerto COM
    ventana.destroy()     # Cerramos la ventana

# --- 4. Creación de la Interfaz Gráfica ---
ventana = tk.Tk()
ventana.title("Control del LED")
ventana.geometry("400x200")

# Interceptar el botón "X" de la ventana para cerrar el puerto serial
ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Etiqueta de título
etiqueta = tk.Label(ventana, text="Control de Actuadores", font=("Arial", 12))
etiqueta.pack(pady=15)

boton_on = tk.Button(ventana, text="Encender LED", command=enviar_encendido, bg="lightgreen", width=15)
boton_on.pack(pady=10)

boton_off = tk.Button(ventana, text="Apagar LED", command=enviar_apagado, bg="salmon", width=15)
boton_off.pack(pady=10)

boton_titilar = tk.Button(ventana, text="Titilar", command=enviar_titilar, bg="brown4", width=15)
boton_titilar.pack(pady=10)


# Iniciamos el bucle de la interfaz
ventana.mainloop()

