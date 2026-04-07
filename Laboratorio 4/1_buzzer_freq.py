from machine import Pin, PWM
from time import sleep

# Configuración del pin GP0 para salida PWM
buzzer = PWM(Pin(0))

# Establecer la frecuencia del tono (1000 Hz)
buzzer.freq(1000)

print("Iniciando prueba de buzzer (Presiona Ctrl+C para detener)")

try:
    while True:
        # Encender el buzzer (Ciclo de trabajo al 50% de 65535)
        buzzer.duty_u16(32768)
        sleep(1)
        
        # Apagar el buzzer (Ciclo de trabajo al 0%)
        buzzer.duty_u16(0)
        sleep(1)

except KeyboardInterrupt:
    # Apagar el buzzer de forma segura si el usuario detiene el programa
    buzzer.duty_u16(0)
    print("\nPrograma detenido.")