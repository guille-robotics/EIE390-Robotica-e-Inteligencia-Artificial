from machine import ADC
from time import sleep
sensor_temp=ADC(4)

while(True):
    valor_raw= sensor_temp.read_u16()*3.3/65535 #3.3 corresponde al voltaje de la Pico, 65535 corresponde a 2^16 -1 (numero de bits)
    temperatura= 27-(valor_raw-0.706)/0.001721 #Fórmula desde el datasheet
    print(f"La Temperatura es: {temperatura}")
    sleep(1)