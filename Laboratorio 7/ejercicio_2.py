from machine import Pin
import time

# Configuración de pines
# Pin GP27 como entrada para leer el sensor PIR
pir_sensor = Pin(27, Pin.IN)

# Pin GP15 como salida para encender el LED
led_indicador = Pin(15, Pin.OUT)

print("Iniciando sistema de alarma visual...")
print("Esperando estabilización del sensor (3 segundos)...")
time.sleep(3)
print("Sistema activo. Monitoreando...")

try:
    while True:
        # Si el sensor detecta movimiento (estado 1)
        if pir_sensor.value() == 1:
            led_indicador.value(1)  # Encender el LED
            print("¡Movimiento detectado! - LED ENCENDIDO")
            
        # Si no hay movimiento (estado 0)
        else:
            led_indicador.value(0)  # Apagar el LED
            print("Zona despejada - LED APAGADO")
            
        # Pausa corta para lectura estable
        time.sleep(0.5)

except KeyboardInterrupt:
    # Apagar el LED por seguridad si se detiene el programa con Ctrl+C
    led_indicador.value(0)
    print("\nPrograma detenido. LED apagado de forma segura.")