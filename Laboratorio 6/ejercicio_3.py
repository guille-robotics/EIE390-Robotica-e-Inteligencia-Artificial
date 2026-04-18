from machine import Pin, time_pulse_us
import time

# Configuración del Ultrasónico
pin_trig = Pin(2, Pin.OUT)
pin_echo = Pin(3, Pin.IN)

# Configuración de los 4 LEDs
led_1 = Pin(4, Pin.OUT)
led_2 = Pin(5, Pin.OUT)
led_3 = Pin(6, Pin.OUT)
led_4 = Pin(7, Pin.OUT)

# Función para apagar todos los LEDs
def apagar_leds():
    led_1.value(0)
    led_2.value(0)
    led_3.value(0)
    led_4.value(0)

def medir_distancia():
    pin_trig.value(0)
    time.sleep_us(2)
    pin_trig.value(1)
    time.sleep_us(10)
    pin_trig.value(0)
    duracion = time_pulse_us(pin_echo, 1, 30000)
    if duracion < 0:
        return 999
    return (duracion * 0.0343) / 2

while True:
    dist = medir_distancia()
    print("Distancia: {:.1f} cm".format(dist))
    
    # Primero apagamos todo por defecto
    apagar_leds()
    
    # Encendido secuencial según la distancia
    if dist <= 5:
        # Menos de 5cm: Los 4 LEDs encendidos
        led_1.value(1)
        led_2.value(1)
        led_3.value(1)
        led_4.value(1)
    elif dist <= 10:
        # Entre 5cm y 10cm: 3 LEDs encendidos
        led_1.value(1)
        led_2.value(1)
        led_3.value(1)
    elif dist <= 15:
        # Entre 10cm y 15cm: 2 LEDs encendidos
        led_1.value(1)
        led_2.value(1)
    elif dist <= 20:
        # Entre 15cm y 20cm: 1 LED encendido
        led_1.value(1)
        
    time.sleep(0.1) # Pequeña pausa para no saturar la consola