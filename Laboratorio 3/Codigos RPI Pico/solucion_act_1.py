import machine
import sys
import uselect
import time

# Configuración de periféricos
led_rojo = machine.Pin(0, machine.Pin.OUT)
led_verde = machine.Pin(1, machine.Pin.OUT)
led_amarillo = machine.Pin(2, machine.Pin.OUT)
led_azul = machine.Pin(3, machine.Pin.OUT)
led_blanco = machine.Pin(4, machine.Pin.OUT)
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
        
        if cmd == "rojo on":
            led_rojo.value(1)
        elif cmd == "rojo off":
            led_rojo.value(0)
        elif cmd == "verde on":
            led_verde.value(1)
        elif cmd == "verde off":
            led_verde.value(0)
        elif cmd == "amarillo on":
            led_amarillo.value(1)
        elif cmd == "amarillo off": 
            led_amarillo.value(0)
        elif cmd == "azul on":
            led_azul.value(1)
        elif cmd == "azul off": 
            led_azul.value(0)
        elif cmd == "blanco on":
            led_blanco.value(1)
        elif cmd == "blanco off": 
            led_blanco.value(0)
        else:
            print(f"Error: Comando '{cmd}' no reconocido")
    
    time.sleep(0.1)