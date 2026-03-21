import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. Configuración de Variables Globales ---
PUERTO = 'COM3'     # Recordar a los alumnos ajustar esto
BAUDIOS = 115200

# Listas para almacenar los datos del gráfico
# Guardaremos los últimos 50 datos para que el gráfico "avance" dinámicamente
max_datos = 50 
datos_y = [0] * max_datos  # Inicializamos la lista de temperaturas con ceros

# --- 2. Inicialización del Puerto Serial ---
try:
    s = serial.Serial(PUERTO, BAUDIOS, timeout=0.1)
    time.sleep(2) # Pausa obligatoria para que la Pico inicie
    print(f"Escuchando telemetría en {PUERTO}...")
except serial.SerialException:
    print(f"Error: No se pudo abrir {PUERTO}.")
    exit() # Salimos del programa si no hay conexión

# --- 3. Configuración del Gráfico (Matplotlib) ---
# Creamos la figura y el eje donde vamos a dibujar
fig, ax = plt.subplots()
ax.set_title("Telemetría en Tiempo Real: Temperatura RP2040")
ax.set_ylabel("Temperatura (°C)")
ax.set_xlabel("Muestras")
ax.set_ylim(15, 30) # Fijamos el eje Y entre 15°C y 45°C para que no salte visualmente

# Creamos el objeto 'linea' que iremos actualizando. 
# Le pasamos un rango para X (0 a 50) y nuestra lista vacía para Y
linea, = ax.plot(range(max_datos), datos_y, color='red', marker='o', markersize=3)

# --- 4. Función de Actualización (El "motor" del gráfico) ---
# Esta función es llamada automáticamente por FuncAnimation cada ciertos milisegundos
def actualizar_grafico(frame):
    global datos_y
    
    nuevo_dato = None
    
    # Leemos TODOS los datos que hayan llegado al buffer serial
    # Esto evita que el gráfico se quede "atrasado" respecto a la Pico
    while s.in_waiting > 0:
        linea_serial = s.readline().decode('utf-8').strip()
        if linea_serial: # Si no está vacía
            try:
                # Convertimos el texto recibido a un número decimal (float)
                nuevo_dato = float(linea_serial)
            except ValueError:
                pass # Si llega basura (ej. el mensaje de inicio), lo ignoramos
                
    # Si logramos leer un dato válido en este ciclo
    if nuevo_dato is not None:
        # Agregamos el nuevo dato al final de la lista
        datos_y.append(nuevo_dato)
        # Eliminamos el primer dato de la lista para mantener el tamaño en 50
        datos_y.pop(0)
        
        # Actualizamos la línea del gráfico con la nueva lista de datos Y
        linea.set_ydata(datos_y)
        
    return linea,

# --- 5. Bucle de Animación ---
# FuncAnimation crea un bucle en segundo plano que llama a 'actualizar_grafico'
# interval=100 significa que intentará actualizarse cada 100 ms
ani = animation.FuncAnimation(fig, actualizar_grafico, interval=100, blit=False)

# Mostramos la ventana del gráfico. Esto detiene el código aquí hasta que se cierre la ventana
plt.show()

# --- 6. Cierre Seguro ---
# Esta línea se ejecuta solo cuando el usuario cierra la ventana del gráfico
s.close()
print("Conexión serial cerrada.")