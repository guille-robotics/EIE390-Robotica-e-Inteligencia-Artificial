import serial
import time

s = serial.Serial(
    port='COM3',       # Cambia al puerto de tu Pico
    baudrate=115200,
    timeout=2,
    dsrdtr=False       # ← Esta línea evita que la Pico se resetee al conectar
)

time.sleep(2)  # Esperamos que la Pico esté lista

while True:
    cmd = input("Comando (on/off/salir): ").strip()

    if cmd.lower() == "salir":
        break

    s.write((cmd + '\r\n').encode())  # Enviamos el comando
    respuesta = s.readline().decode().strip()  # Esperamos respuesta
    print("Pico:", respuesta)

s.close()
