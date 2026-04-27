from machine import Pin
import time
from servo import Servo

# ==========================================
# CONFIGURACIÓN DE COMPONENTES
# ==========================================
pir_sensor = Pin(27, Pin.IN)
led_luz = Pin(15, Pin.OUT)
puerta_servo = Servo(16)

# OPCIONAL: Pin para un buzzer (si decides agregarlo)
# buzzer = Pin(14, Pin.OUT)

# ==========================================
# INICIALIZACIÓN
# ==========================================
print("Calibrando sistema...")
# Sugerencia de desafío: Hacer que el LED parpadee aquí
time.sleep(3) 
print("Sistema en línea.")

try:
    while True:
        if pir_sensor.value() == 1:
            print("Acceso concedido: Abriendo puerta...")
            led_luz.value(1)       # Encendemos luz
            puerta_servo.move(90)  # Abrimos puerta
            
            # --- JUEGA AQUÍ ---
            # ¿Cuánto tiempo quieres que la puerta se quede abierta?
            time.sleep(2) 
            
        else:
            # --- JUEGA AQUÍ ---
            # Puedes agregar un retardo aquí antes de cerrar para 
            # que la luz no se apague de inmediato.
            led_luz.value(0)
            puerta_servo.move(0)
            
        time.sleep(0.1) # Pequeña pausa de estabilidad

except KeyboardInterrupt:
    led_luz.value(0)
    puerta_servo.move(0)
    puerta_servo.stop()
    print("\nSistema desactivado.")