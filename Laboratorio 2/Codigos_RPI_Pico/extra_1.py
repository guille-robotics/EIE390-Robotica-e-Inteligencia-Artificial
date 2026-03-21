import machine
import sys
import uselect
import time

led = machine.Pin(25, machine.Pin.OUT)
spoll = uselect.poll()
spoll.register(sys.stdin, uselect.POLLIN)

print("Pico: Sistema listo. Comandos: on, off, titilar, titilar <ms>")

# Variables para el parpadeo (máquina de estados simple)
blinking = False
blink_interval = 500  # Intervalo por defecto en milisegundos
last_blink_time = time.ticks_ms()

while True:
    # 1. ETAPA DE LECTURA (Polling rápido con timeout 0)
    if spoll.poll(0):
        line = sys.stdin.readline().strip().lower()
        if line:
            # Separamos el string por espacios. Ej: ["titilar", "200"]
            partes = line.split()
            cmd = partes[0]
            
            if cmd == "on":
                blinking = False
                led.value(1)
                print("ACK: LED Encendido")
            elif cmd == "off":
                blinking = False
                led.value(0)
                print("ACK: LED Apagado")
            elif cmd == "titilar":
                blinking = True
                # Verificamos si mandaron un segundo argumento y si es un número
                if len(partes) > 1 and partes[1].isdigit():
                    blink_interval = int(partes[1])
                    print(f"ACK: Titilando cada {blink_interval} ms")
                else:
                    blink_interval = 500
                    print("ACK: Titilando a 500 ms (por defecto)")
            else:
                print(f"Error: Comando '{cmd}' no reconocido")

    # 2. ETAPA DE EJECUCIÓN CONTINUA (Parpadeo asíncrono)
    if blinking:
        current_time = time.ticks_ms()
        # Calculamos la diferencia de tiempo sin bloquear el procesador
        if time.ticks_diff(current_time, last_blink_time) >= blink_interval:
            led.toggle()  # Cambia el estado del LED (de 1 a 0, o de 0 a 1)
            last_blink_time = current_time