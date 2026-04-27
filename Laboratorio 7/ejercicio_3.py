from machine import Pin
import time
from servo import Servo  # Importamos la clase Servo desde el archivo servo.py

# ==========================================
# CONFIGURACIÓN DE PINES Y COMPONENTES
# ==========================================
# 1. Sensor PIR (Entrada)
pir_sensor = Pin(27, Pin.IN)

# 2. Diodo LED (Salida)
led_luz = Pin(15, Pin.OUT)

# 3. Servomotor (Salida PWM mediante la clase importada)
puerta_servo = Servo(16)

# ==========================================
# INICIALIZACIÓN DEL SISTEMA
# ==========================================
print("Iniciando Sistema Domótico...")
led_luz.value(0)       # Aseguramos que la luz inicie apagada
puerta_servo.move(0)   # Aseguramos que la puerta inicie cerrada (0 grados)

print("Calibrando sensor PIR (3 segundos)...")
time.sleep(3)
print("Sistema activo. Esperando movimiento...")

# ==========================================
# BUCLE PRINCIPAL DE CONTROL
# ==========================================
try:
    while True:
        # Leemos el estado del sensor PIR
        if pir_sensor.value() == 1:
            print("¡Persona detectada! Encendiendo luz y abriendo puerta.")
            led_luz.value(1)       # Enciende la luz
            puerta_servo.move(90)  # Abre la puerta (90 grados)
            
        else:
            print("Zona despejada. Apagando luz y cerrando puerta.")
            led_luz.value(0)       # Apaga la luz
            puerta_servo.move(0)   # Cierra la puerta (0 grados)
            
        # Breve pausa para no saturar las lecturas y dar tiempo al mecanismo
        time.sleep(0.5)

except KeyboardInterrupt:
    # Rutina de seguridad si el usuario detiene el programa (Ctrl+C)
    print("\nDeteniendo sistema. Cerrando accesos...")
    led_luz.value(0)       # Apagamos la luz
    puerta_servo.move(0)   # Cerramos la puerta
    time.sleep(0.5)        # Damos medio segundo para que el servo termine de moverse
    puerta_servo.stop()    # Desactivamos el PWM del servo usando el método de la clase