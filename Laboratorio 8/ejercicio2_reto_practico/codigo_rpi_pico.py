from machine import Pin
import sys
import select
import time

# 1. Configuración de los actuadores
# LED 1: Configurado para la primera parte de la Actividad 2
led_1 = Pin(15, Pin.OUT)

# LED 2: Configurado para el Reto Práctico
led_2 = Pin(14, Pin.OUT)

# Nos aseguramos de que ambos inicien apagados por seguridad
led_1.value(0)
led_2.value(0)

# 2. Bucle principal infinito
while True:
    
    # 3. Lectura no bloqueante del puerto Serial (USB)
    # select.select revisa si el servidor FastAPI envió algo por USB (sys.stdin)
    # El '0' al final evita que la placa se quede congelada esperando datos.
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        
        # Leemos exactamente 1 byte (1 carácter) del puerto serial
        comando = sys.stdin.read(1) 
        
        # 4. Lógica de control físico para LED 1 (Base)
        if comando == 'E':
            led_1.value(1) # Enciende el LED 1
            
        elif comando == 'A':
            led_1.value(0) # Apaga el LED 1
            
        # 5. Lógica de control físico para LED 2 (Reto Práctico)
        elif comando == 'X':
            led_2.value(1) # Enciende el LED 2
            
        elif comando == 'Y':
            led_2.value(0) # Apaga el LED 2

    # Una pequeñísima pausa para estabilizar el sistema y no sobrecargar la Pico
    time.sleep(0.05)