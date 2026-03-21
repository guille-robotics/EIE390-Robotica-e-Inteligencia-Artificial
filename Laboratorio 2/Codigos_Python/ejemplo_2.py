#Usando codigo no bloqueante
import serial
import time

try:
    s = serial.Serial(
        port='COM3', # Cambiar según corresponda
        baudrate=115200,
        timeout=1,
        dsrdtr=False
    )
    time.sleep(2) # Pausa para inicialización
    
    print("Conectado a la Pico. Escriba 'on', 'off' o 'salir'.")

    while True:
        cmd = input(">> ").strip().lower()

        if cmd == "salir":
            break

        if cmd:
            s.write((cmd + '\r\n').encode())
            # Esperamos la respuesta de confirmación (ACK)
            respuesta = s.readline().decode().strip()
            if respuesta:
                print(f"Respuesta: {respuesta}")

    s.close()
    print("Conexión cerrada.")

except serial.SerialException as e:
    print(f"Error de conexión: {e}")