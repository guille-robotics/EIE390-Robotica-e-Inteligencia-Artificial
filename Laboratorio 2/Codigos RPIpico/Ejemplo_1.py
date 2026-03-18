from machine import Pin
import sys
import time

led = Pin(25, Pin.OUT)

print("Pico lista")

while True:
    # readline() espera hasta recibir una línea completa, simple y directo
    cmd = sys.stdin.readline().strip().lower()
   # cmd=input().strip().lower() # ESTO GENERA ECO 

    if cmd == "on":
        led.value(1)
        print("Encendido")
    elif cmd == "off":
        led.value(0)
        print("Apagado")
    else:
        print("Comando desconocido")
