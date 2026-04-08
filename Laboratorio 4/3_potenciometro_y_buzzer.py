from machine import Pin, PWM, ADC
from time import sleep

# Configurar pines
buzzer = PWM(Pin(0))
potenciometro = ADC(Pin(26))

# Función para adaptar rangos (equivalente a map() en Arduino)
# Convierte un valor de un rango original a un rango destino
def mapear(valor, in_min, in_max, out_min, out_max):
    return int((valor - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

print("Iniciando control de tono... (Ctrl+C para detener)")

try:
    # Encender el buzzer a volumen medio (50% de 65535)
    buzzer.duty_u16(32768)
    
    while True:
        # 1. Leer el valor del ADC (0 a 65535)
        lectura_adc = potenciometro.read_u16()
        
        # 2. Mapear la lectura a frecuencias audibles (ej. 200 Hz a 2000 Hz)
        # Evitamos frecuencias muy bajas (<100Hz) porque el buzzer no las reproduce bien
        nueva_frecuencia = mapear(lectura_adc, 0, 65535, 200, 2000)
        
        # 3. Asignar la nueva frecuencia al buzzer
        buzzer.freq(nueva_frecuencia)
        
        # 4. Imprimir valores en terminal para visualizar los cambios
        print(f"ADC: {lectura_adc:5d}  ->  Frecuencia: {nueva_frecuencia:4d} Hz")
        
        # Pequeña pausa para estabilidad
        sleep(0.05)

except KeyboardInterrupt:
    # Apagar el sonido al detener el programa
    buzzer.duty_u16(0)
    print("\nPrograma detenido.")