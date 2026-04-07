import tkinter as tk
import serial
import time

# ======================================================================
# 1. CONFIGURACIÓN DEL PUERTO SERIAL
# ======================================================================
# Intentamos abrir la conexión con la Raspberry Pi Pico.
# Usamos un bloque try-except para que el programa no colapse (crashee) 
# si el alumno pone el puerto equivocado o la placa está desconectada.
try:
    # IMPORTANTE: Cambiar 'COM3' por el puerto real asignado por el sistema operativo
    # 115200 es la velocidad (baudrate) estándar de MicroPython.
    # timeout=1 evita que el programa se quede esperando infinitamente si no hay respuesta.
    puerto_serial = serial.Serial('COM3', 115200, timeout=1, dsrdtr=False)
    
    # Pausa de 2 segundos: Al abrir el puerto serial, algunas placas se reinician.
    # Este tiempo le da "respiro" a la Pico para iniciar su código antes de mandarle datos.
    time.sleep(2) 
    print("Conexión serial establecida correctamente.")
except serial.SerialException:
    print("ERROR: No se pudo abrir el puerto. Verifica que la placa esté conectada y el puerto sea correcto.")

# ======================================================================
# 2. FUNCIÓN LÓGICA (EL MENSAJERO)
# ======================================================================
# Esta es la única función que necesitamos para enviar cualquier comando.
# Recibe el texto exacto que queremos mandar, por ejemplo: "rojo on"
def enviar_comando(instruccion):
    # Agregamos "\r\n" al final. Es el equivalente a presionar la tecla "Enter".
    # La Raspberry Pi Pico necesita esto para saber que el comando terminó.
    comando_completo = f"{instruccion}\r\n"
    
    # Validamos de forma segura que la variable del puerto exista y esté abierta
    if 'puerto_serial' in globals() and puerto_serial.is_open:
        # Los puertos seriales no entienden texto puro, solo entienden bytes (unos y ceros).
        # Usamos .encode('utf-8') para traducir nuestro texto a bytes antes de enviarlo.
        puerto_serial.write(comando_completo.encode('utf-8'))
        print(f"Enviado al hardware: {instruccion}")
    else:
        print(f"Simulando envío (Puerto cerrado): {instruccion}")

# ======================================================================
# 3. FUNCIÓN DE LIMPIEZA Y CIERRE
# ======================================================================
# Si cerramos la ventana a la fuerza, el puerto serial del PC puede quedar "atrapado".
# Esta función asegura que el puerto se libere correctamente para poder volver a usarlo.
def cerrar_aplicacion():
    if 'puerto_serial' in globals() and puerto_serial.is_open:
        puerto_serial.close() # Soltamos el puerto COM
        print("Puerto serial cerrado de forma segura.")
    ventana.destroy() # Finalmente, destruimos la ventana gráfica

# ======================================================================
# 4. CREACIÓN DE LA INTERFAZ GRÁFICA (GUI)
# ======================================================================
# Inicializamos el motor de Tkinter
ventana = tk.Tk()
ventana.title("Panel de Control de Actuadores") # Título de la ventana
ventana.geometry("350x400") # Ancho x Alto en píxeles

# Interceptamos el botón "X" (cerrar) de la ventana de Windows/Mac/Linux.
# En lugar de cerrar de golpe, le decimos que ejecute nuestra función de limpieza primero.
ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Etiqueta principal de título dentro de la ventana
tk.Label(ventana, text="Control Serial de LEDs", font=("Arial", 14, "bold")).pack(pady=15)

# ======================================================================
# 5. GENERACIÓN DINÁMICA DE BOTONES (EL DESAFÍO)
# ======================================================================
# Creamos una lista que contiene todos los datos de nuestros LEDs.
# Cada elemento es una tupla: (Nombre del comando, Color de encendido, Color de apagado)
colores_leds = [
    ("rojo", "red", "lightcoral"),
    ("verde", "green", "lightgreen"),
    ("amarillo", "yellow", "lightyellow"),
    ("azul", "blue", "lightblue"),
    ("blanco", "white", "lightgray")
]

# Usamos un bucle FOR para no tener que escribir el código del botón 10 veces seguidas.
for nombre, color_on, color_off in colores_leds:
    
    # Frame: Es como una "caja" invisible que usamos para poner botones uno al lado del otro.
    fila = tk.Frame(ventana)
    fila.pack(pady=5) # Separación vertical entre filas
    
    # Botón de ENCENDIDO
    # TRUCO CLAVE: lambda n=nombre. Esto congela el valor del nombre en esta iteración exacta.
    # Si solo usamos lambda: enviar_comando(nombre), todos los botones enviarían el último color ("blanco").
    btn_on = tk.Button(fila, text=f"{nombre.upper()} ON", 
                       command=lambda n=nombre: enviar_comando(f"{n} on"), 
                       bg=color_on, width=12)
    btn_on.pack(side=tk.LEFT, padx=10) # side=tk.LEFT los alínea horizontalmente en su fila

    # Botón de APAGADO
    btn_off = tk.Button(fila, text=f"{nombre.upper()} OFF", 
                        command=lambda n=nombre: enviar_comando(f"{n} off"), 
                        bg=color_off, width=12)
    btn_off.pack(side=tk.LEFT, padx=10)

# Botón maestro para apagar todos los LEDs usando una comprensión de listas en Python
tk.Button(ventana, text="APAGAR TODOS", 
          command=lambda: [enviar_comando(f"{c[0]} off") for c in colores_leds], 
          bg="black", fg="white", width=25).pack(pady=20)

# Botón maestro para encender todos los LEDs usando una comprensión de listas en Python
tk.Button(ventana, text="PRENDER TODOS", 
          command=lambda: [enviar_comando(f"{c[0]} on") for c in colores_leds], 
          bg="red", fg="black", width=25).pack(pady=20)

# Iniciamos el bucle infinito de la interfaz gráfica para que espere los clics del usuario
ventana.mainloop()