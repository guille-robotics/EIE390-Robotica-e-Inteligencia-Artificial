import machine
import time

# --- 1. Configuración del Hardware ---
# El sensor de temperatura interno está conectado al ADC 4 en la Raspberry Pi Pico
sensor_temp = machine.ADC(4)

# Factor de conversión para pasar de los 16 bits del ADC (0-65535) a Voltaje (0-3.3V)
factor_conversion = 3.3 / 65535

# Variable para llevar el control del tiempo (Polling no bloqueante)
ultimo_envio = time.ticks_ms()
intervalo_envio = 100  # Enviaremos datos cada 100 milisegundos (10 Hz)

print("Pico: Iniciando telemetría de temperatura...")

# --- 2. Bucle Principal ---
while True:
    tiempo_actual = time.ticks_ms()
    
    # Verificamos si ya pasaron los 100 ms desde el último envío
    if time.ticks_diff(tiempo_actual, ultimo_envio) >= intervalo_envio:
        
        # Leemos el valor en bruto del ADC (un número entre 0 y 65535)
        lectura_16bits = sensor_temp.read_u16()
        
        # Convertimos esa lectura a Voltaje
        voltaje = lectura_16bits * factor_conversion
        
        # Fórmula del datasheet de la Raspberry Pi Pico (RP2040)
        # 27 grados menos la diferencia de voltaje respecto a 0.706V
        temperatura_celsius = 27 - (voltaje - 0.706) / 0.001721
        
        # Imprimimos el dato por serial. 
        # NOTA: print() añade automáticamente el \r\n al final
        # Usamos round() para enviar solo 2 decimales y limpiar el ruido
        print(round(temperatura_celsius, 2))
        
        # Actualizamos el cronómetro
        ultimo_envio = tiempo_actual