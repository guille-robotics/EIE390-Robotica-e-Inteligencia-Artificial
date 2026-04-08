from machine import Pin, PWM, ADC
from time import sleep

# Configurar pines
buzzer = PWM(Pin(0))
potenciometro = ADC(Pin(26))

# Establecer una frecuencia fija constante (Tono de 1000 Hz)
buzzer.freq(1000)

# Función para adaptar rangos
def mapear(valor, in_min, in_max, out_min, out_max):
    return int((valor - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

print("Iniciando control de volumen... (Ctrl+C para detener)")

try:
    while True:
        # 1. Leer el valor del ADC (0 a 65535)
        lectura_adc = potenciometro.read_u16()
        
        # 2. Mapear la lectura al volumen (Ciclo de trabajo o Duty Cycle)
        # 0 = Silencio absoluto (0%)
        # 32768 = Volumen máximo acústico (50% de la señal PWM)
        nuevo_volumen = mapear(lectura_adc, 0, 65535, 0, 32768)
        
        # 3. Asignar el nuevo volumen al buzzer
        buzzer.duty_u16(nuevo_volumen)
        
        # 4. Calcular el porcentaje del 0 al 100% para mostrar en la terminal
        porcentaje_vol = int((nuevo_volumen / 32768) * 100)
        
        # Imprimir valores para visualizar los cambios
        print(f"ADC: {lectura_adc:5d}  ->  Volumen: {porcentaje_vol:3d}%")
        
        # Pequeña pausa para estabilidad
        sleep(0.05)

except KeyboardInterrupt:
    # Apagar el sonido al detener el programa
    buzzer.duty_u16(0)
    print("\nPrograma detenido.")
