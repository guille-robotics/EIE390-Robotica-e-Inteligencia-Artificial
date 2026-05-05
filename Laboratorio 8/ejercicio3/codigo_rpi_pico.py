from machine import Pin, ADC
import sys
import select
import time


# Configuración del Sensor (ADC)
# El pin GP26 corresponde al canal 0 del Conversor Analógico Digital (ADC)
sensor_adc = ADC(26) 

print("Iniciando sistema bidireccional...")

while True:
    # --- ENVÍO DE DATOS SENSORIALES (Pico -> Web) ---
    # Lee el valor del potenciómetro o sensor de humedad (Rango 0 a 65535)
    valor = sensor_adc.read_u16()
    
    # La función print() envía el dato automáticamente por el cable USB (Serial)
    # y le agrega un salto de línea (\n) al final.
    print(valor) 

    # Pausa de 100ms. Es vital para no colapsar el buffer de la computadora.
    time.sleep(0.1)