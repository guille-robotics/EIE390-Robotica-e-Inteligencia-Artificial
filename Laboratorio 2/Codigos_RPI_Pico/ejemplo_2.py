import machine
import sys
import uselect
import time

# Configuración de periféricos
led = machine.Pin(25, machine.Pin.OUT)

# Creamos un objeto de sondeo (poll)
spoll = uselect.poll()
# Registramos la entrada estándar para eventos de lectura (POLLIN)
spoll.register(sys.stdin, uselect.POLLIN)

print("Pico: Sistema No Bloqueante Listo")

while True:
    # Verificamos si hay datos esperando (espera máxima de 10ms)
    if spoll.poll(10):
        # Leemos solo cuando estamos seguros de que hay una línea
        cmd = sys.stdin.readline().strip().lower()
        
        if cmd == "on":
            led.value(1)
            print("ACK: LED Encendido")
        elif cmd == "off":
            led.value(0)
            print("ACK: LED Apagado")
        else:
            print(f"Error: Comando '{cmd}' no reconocido")
    
    time.sleep(0.1)