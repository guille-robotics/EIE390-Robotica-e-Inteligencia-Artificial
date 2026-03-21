import machine
import sys
import uselect
import time

led = machine.Pin(25, machine.Pin.OUT)
spoll = uselect.poll()
spoll.register(sys.stdin, uselect.POLLIN)

print("Pico: Sistema No Bloqueante Listo")

# Variables para el desafío
estado_titilar = False
ultimo_tiempo = time.ticks_ms()

while True:
    # LECTURA SERIAL (Timeout bajado a 0 o 10 para fluidez)
    if spoll.poll(10):
        cmd = sys.stdin.readline().strip().lower()
        
        if cmd == "on":
            estado_titilar = False # Fundamental apagar el flag
            led.value(1)
            print("ACK: LED Encendido")
        elif cmd == "off":
            estado_titilar = False # Fundamental apagar el flag
            led.value(0)
            print("ACK: LED Apagado")
        elif cmd == "titilar":
            estado_titilar = True  # Activamos el flag
            print("ACK: Modo Titilar Activado")
        else:
            print(f"Error: Comando '{cmd}' no reconocido")
    
    # EJECUCIÓN DEL PARPADEO (No bloqueante)
    if estado_titilar:
        tiempo_actual = time.ticks_ms()
        if time.ticks_diff(tiempo_actual, ultimo_tiempo) >= 500:
            led.toggle() # Cambia de 1 a 0, o de 0 a 1
            ultimo_tiempo = tiempo_actual # Reinicia el cronómetro
