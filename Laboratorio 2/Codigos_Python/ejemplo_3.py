import serial
import time

try:
    s = serial.Serial(
        port='COM3', # Recuerda a los alumnos cambiar su puerto
        baudrate=115200,
        timeout=0.1, # Timeout corto para fluidez
        dsrdtr=False
    )
    time.sleep(2)
    
    print("Conectado. Ejemplos de comandos: 'on', 'off', 'titilar', 'titilar 200', 'salir'")

    while True:
        cmd = input(">> ").strip().lower()

        if cmd == "salir":
            break

        if cmd:
            s.write((cmd + '\r\n').encode())
            time.sleep(0.05) # Pausa mínima para que la Pico procese
            
            # Leemos todas las líneas que la Pico haya enviado de vuelta
            while s.in_waiting > 0:
                respuesta = s.readline().decode().strip()
                if respuesta:
                    print(f"Pico dice: {respuesta}")

    s.close()
    print("Conexión cerrada.")

except serial.SerialException as e:
    print(f"Error: {e}")