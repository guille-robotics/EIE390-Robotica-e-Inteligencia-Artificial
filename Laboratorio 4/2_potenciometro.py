from machine import Pin, ADC
from time import sleep

# Configurar el pin GP26 como entrada analógica (ADC0)
potenciometro = ADC(Pin(26))

print("Iniciando lectura del potenciómetro...")
print("Presiona Ctrl+C para detener.")

try:
    while True:
        # 1. Leer el valor crudo del ADC (rango de 0 a 65535)
        valor_crudo = potenciometro.read_u16()
        
        # 2. Transformar (mapear) el valor a un rango de 0 a 100
        # Fórmula: (valor_actual / valor_maximo) * 100
        porcentaje = int((valor_crudo / 65535) * 100)
        
        # 3. Imprimir los resultados en la consola
        print(f"Lectura ADC: {valor_crudo:5d}  |  Porcentaje: {porcentaje:3d}%")
        
        # 4. Pequeña pausa para no saturar la consola
        sleep(0.1)

except KeyboardInterrupt:
    print("\nLectura detenida.")