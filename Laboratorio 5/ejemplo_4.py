from servo import Servo
from time import sleep
import sys

# 1. Crear los objetos Servo en pines distintos (ej. GP0 y GP1)
servo1 = Servo(pin=0)
servo2 = Servo(pin=1)

print("--- Control de Múltiples Servos por Serial ---")
print("Formato de comando: 'motor, ángulo'")
print("Ejemplo: '1,90' (mueve el motor 1 a 90 grados)")
print("Ejemplo: '2,180' (mueve el motor 2 a 180 grados)")
print("Ingresa 'salir' para detener.")
print("-" * 40)

try:
    while True:
        # Leer el comando desde el monitor serial
        cmd = sys.stdin.readline().strip().lower()
        
        # Condición de salida
        if cmd == 'salir':
            print("Saliendo del programa...")
            break
            
        # Procesar el comando
        try:
            # Ignorar entradas vacías
            if cmd == "":
                continue
                
            # Separar el texto ingresado usando la coma como divisor
            partes = cmd.split(',')
            
            # Validar que efectivamente se ingresaron dos valores
            if len(partes) != 2:
                print("Error de formato. Usa 'motor,angulo' (ej: '1,90')")
                continue
            
            # Convertir las partes separadas a números enteros
            motor_id = int(partes[0].strip())
            angulo = int(partes[1].strip())
            
            # Validar que el ángulo esté en rango
            if 0 <= angulo <= 180:
                # Dirigir el comando al servo correspondiente
                if motor_id == 1:
                    print(f"Moviendo Servo 1 (Pin 0) a: {angulo}°")
                    servo1.move(angulo)
                elif motor_id == 2:
                    print(f"Moviendo Servo 2 (Pin 1) a: {angulo}°")
                    servo2.move(angulo)
                else:
                    print("Error: El ID del motor debe ser 1 o 2.")
            else:
                print("Error: El ángulo debe estar entre 0 y 180.")
                
        except ValueError:
            # Esto atrapa el error si escriben letras como 'uno,noventa'
            print(f"Entrada inválida: '{cmd}'. Asegúrate de usar solo números.")
            
except KeyboardInterrupt:
    print("\nInterrupción por teclado (Ctrl+C).")

finally:
    # Es vital apagar AMBOS motores al terminar
    servo1.stop()
    servo2.stop()
    print("PWM detenido en ambos motores. Programa finalizado.")
