from servo import Servo
from time import sleep
import sys

# Crear el objeto Servo en el pin 0 (asegúrate de que coincida con el hardware de los alumnos)
servo = Servo(pin=0)

print("--- Control de Servo por Serial ---")
print("Ingresa un ángulo entre 0 y 180 (o 'salir' para detener):")

try:
    while True:
        # 1. Leer el comando desde el monitor serial (Thonny, PuTTY, etc.)
        cmd = sys.stdin.readline().strip().lower()
        
        # 2. Condición de salida segura
        if cmd == 'salir':
            print("Saliendo del programa...")
            break
            
        # 3. Intentar convertir el texto a un número y mover el servo
        try:
            angulo = int(cmd)
            
            # Validar que el ángulo esté dentro del rango permitido
            if 0 <= angulo <= 180:
                print(f"Moviendo servo a: {angulo}°")
                servo.move(angulo)
            else:
                print("Error: El ángulo debe estar entre 0 y 180.")
                
        except ValueError:
            # Esto evita que el programa colapse si el alumno teclea letras
            if cmd != "": 
                print(f"Entrada inválida: '{cmd}'. Por favor ingresa un número.")
            
except KeyboardInterrupt:
    print("\nInterrupción por teclado (Ctrl+C).")

finally:
    # Apagar el PWM para proteger el motor sin importar cómo termine el script
    servo.stop()
    print("PWM detenido y programa finalizado.")