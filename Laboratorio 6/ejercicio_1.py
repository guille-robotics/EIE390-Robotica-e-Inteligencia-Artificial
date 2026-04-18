from machine import Pin, time_pulse_us
import time

# Configuración de pines
pin_trig = Pin(2, Pin.OUT)
pin_echo = Pin(3, Pin.IN)

def medir_distancia():
    # Aseguramos que el Trigger esté en bajo
    pin_trig.value(0)
    time.sleep_us(2)
    
    # Enviamos un pulso de 10 microsegundos
    pin_trig.value(1)
    time.sleep_us(10)
    pin_trig.value(0)
    
    # Medimos el tiempo que el pin Echo está en ALTO
    duracion = time_pulse_us(pin_echo, 1, 30000) # Timeout de 30ms
    
    # Si duracion es < 0, ocurrió un timeout
    if duracion < 0:
        return -1
        
    # Calculamos la distancia (Velocidad del sonido: 34300 cm/s)
    # Distancia = (Tiempo * Velocidad) / 2
    distancia = (duracion * 0.0343) / 2
    return distancia

while True:
    dist = medir_distancia()
    if dist != -1:
        print("Distancia: {:.1f} cm".format(dist))
    else:
        print("Fuera de rango")
    
    time.sleep(0.5)