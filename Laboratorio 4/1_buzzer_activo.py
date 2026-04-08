from machine import Pin
from time import sleep

# Configuración del pin GP0 como salida digital normal
buzzer = Pin(0, Pin.OUT)

print("Iniciando prueba de buzzer activo (Presiona Ctrl+C para detener)")

try:
    while True:
        buzzer.value(1) # Encender
        sleep(1)
        
        buzzer.value(0) # Apagar
        sleep(1)

except KeyboardInterrupt:
    buzzer.value(0)
    print("\nPrograma detenido.")