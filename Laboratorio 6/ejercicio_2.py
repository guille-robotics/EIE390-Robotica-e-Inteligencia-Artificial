from machine import Pin, time_pulse_us
from servo import Servo  # Importamos la librería servo que creamos en el ejercicio anterior
import time

# Configuración del Ultrasónico
pin_trig = Pin(2, Pin.OUT)
pin_echo = Pin(3, Pin.IN)

# Configuración del Servo en el pin GP0
mi_servo = Servo(pin=0) 

# Umbral de distancia en centímetros
UMBRAL = 10.0 

def medir_distancia():
    pin_trig.value(0)
    time.sleep_us(2)
    pin_trig.value(1)
    time.sleep_us(10)
    pin_trig.value(0)
    duracion = time_pulse_us(pin_echo, 1, 30000)
    if duracion < 0:
        return 999 # Retornamos un valor alto si hay error
    return (duracion * 0.0343) / 2

try:
    while True:
        dist = medir_distancia()
        print("Distancia actual: {:.1f} cm".format(dist))
        
        # Lógica de actuación reactiva
        if dist < UMBRAL:
            print("¡Mano detectada! Abriendo...")
            mi_servo.move(90)  # Posición activa
        else:
            mi_servo.move(0)   # Posición de reposo
            
        time.sleep(0.2)
        
except KeyboardInterrupt:
    print("Programa detenido.")
    mi_servo.move(0) # Retornar a reposo de forma segura