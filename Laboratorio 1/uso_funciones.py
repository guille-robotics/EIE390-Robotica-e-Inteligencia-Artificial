from machine import ADC
from time import sleep
from funciones import c_to_f
sensor_temp=ADC(4)

while(True):
    valor_raw= sensor_temp.read_u16()*3.3/65535 #3.3 corresponde al voltaje de la Pico, 65535 corresponde a 2^16 -1 (numero de bits)
    c_temp= 27-(valor_raw-0.706)/0.001721 #Fórmula desde el datasheet
    far_temp=c_to_f(c_temp)
    print(f"La Temperatura en Celcius es: {c_temp} ")
    print(f"La Temperatura en Farenheit es: {far_temp} ")
    sleep(1)
