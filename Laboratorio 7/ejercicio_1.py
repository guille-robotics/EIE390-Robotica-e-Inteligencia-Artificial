from machine import Pin
import time

# Configuración del pin del sensor PIR
# Utilizamos el pin GP27 (Pin físico 32) como entrada digital
pir_sensor = Pin(27, Pin.IN)

print("Iniciando sensor PIR...")
print("Por favor, espere un momento para que el sensor se estabilice...")
time.sleep(3) # Pequeña pausa para estabilizar la medición infrarroja
print("Sensor listo. Monitoreando el área...")

try:
    while True:
        # Leer el estado digital del sensor
        # 1 = Movimiento detectado, 0 = Zona despejada
        estado = pir_sensor.value()
        
        if estado == 1:
            print("¡Movimiento detectado!")
        else:
            print("Sin movimiento...")
            
        # Pausa para no saturar la consola de Thonny con demasiados mensajes
        time.sleep(0.5)

except KeyboardInterrupt:
    # Permite detener el programa limpiamente con Ctrl+C
    print("\nPrograma detenido por el usuario.")
