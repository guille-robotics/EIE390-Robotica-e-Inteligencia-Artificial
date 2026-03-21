import tkinter as tk
from tkinter import scrolledtext
import serial
import time

# --- 1. Configuración Serial ---
PUERTO = 'COM3'  # Recordar a los alumnos cambiarlo según su PC
BAUDIOS = 115200

try:
    s = serial.Serial(PUERTO, BAUDIOS, timeout=0.1, dsrdtr=False)
    time.sleep(2)  # Pausa vital para que la Pico inicie
    conectado = True
    print("Conexión exitosa a", PUERTO)
except serial.SerialException:
    print(f"Error: No se pudo abrir {PUERTO}. Verifica el cable y el número de COM.")
    conectado = False

# --- 2. Funciones Lógicas ---
def enviar_comando(cmd):
    """Envía el comando por serial a la Pico."""
    if conectado:
        s.write((cmd + '\r\n').encode())

def btn_on():
    enviar_comando("on")

def btn_off():
    enviar_comando("off")

def btn_titilar():
    """Lee el cuadro de texto y envía el comando con o sin argumentos."""
    tiempo_ms = entrada_tiempo.get().strip()
    if tiempo_ms.isdigit():
        enviar_comando(f"titilar {tiempo_ms}")
    else:
        enviar_comando("titilar") # Envía el comando por defecto si está vacío

def leer_puerto_periodicamente():
    """Revisa si hay datos en el puerto serial sin bloquear la GUI."""
    if conectado:
        while s.in_waiting > 0:
            respuesta = s.readline().decode('utf-8').strip()
            if respuesta:
                # Escribimos la respuesta en la consola virtual de la interfaz
                consola.insert(tk.END, f"Pico > {respuesta}\n")
                consola.see(tk.END) # Auto-scroll hacia abajo
    
    # Aquí está la magia: Tkinter volverá a llamar a esta función en 100 ms
    ventana.after(100, leer_puerto_periodicamente)

def cerrar_aplicacion():
    """Asegura que el puerto COM se libere al cerrar la ventana."""
    if conectado:
        s.close()
    ventana.destroy()

# --- 3. Interfaz Gráfica (Tkinter) ---
ventana = tk.Tk()
ventana.title("Panel de Control - Robótica")
ventana.geometry("400x350")
# Manejar el evento de la "X" de la ventana para cerrar el puerto
ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion) 

# --- Elementos Visuales (Widgets) ---
lbl_titulo = tk.Label(ventana, text="Control de Raspberry Pi Pico", font=("Arial", 14, "bold"))
lbl_titulo.pack(pady=10)

# Frame para los botones ON/OFF
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

btn_encender = tk.Button(frame_botones, text="Encender LED", command=btn_on, bg="lightgreen", width=15)
btn_encender.grid(row=0, column=0, padx=5)

btn_apagar = tk.Button(frame_botones, text="Apagar LED", command=btn_off, bg="salmon", width=15)
btn_apagar.grid(row=0, column=1, padx=5)

# Frame para Titilar
frame_titilar = tk.Frame(ventana)
frame_titilar.pack(pady=10)

lbl_ms = tk.Label(frame_titilar, text="Tiempo (ms):")
lbl_ms.grid(row=0, column=0, padx=5)

entrada_tiempo = tk.Entry(frame_titilar, width=10)
entrada_tiempo.grid(row=0, column=1, padx=5)

btn_blink = tk.Button(frame_titilar, text="Enviar Titilar", command=btn_titilar, bg="lightblue")
btn_blink.grid(row=0, column=2, padx=5)

# Consola de respuestas (ScrolledText)
lbl_consola = tk.Label(ventana, text="Respuestas de la Pico:")
lbl_consola.pack()

consola = scrolledtext.ScrolledText(ventana, width=45, height=8, state='normal')
consola.pack(pady=5)

# --- 4. Inicio del Programa ---
if conectado:
    consola.insert(tk.END, f"Sistema conectado en {PUERTO}\n---\n")
    # Iniciar el ciclo de lectura (Polling de Tkinter)
    ventana.after(100, leer_puerto_periodicamente)
else:
    consola.insert(tk.END, "ERROR: No hay conexión. Cierre y revise el puerto.\n")

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()