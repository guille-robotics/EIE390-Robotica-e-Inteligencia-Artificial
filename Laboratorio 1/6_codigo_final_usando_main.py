#Para este código, crearemos un carpeta llamada src y dentro de ella un código llamado funciones
from machine import ADC
from time import sleep
from src.funciones import c_to_f
from src.funciones import c_to_k

def main():

    sensor_temp=ADC(4)
    print("Medidor de Temperaturas (Celsius, Fahrenheit y Kelvin)")
    print("Ingrese el sistema de temperatura deseado")
    print("Comandos: celsius | fahrenheit | kelvin | finalizar")

    while(True):
        valor_raw= sensor_temp.read_u16()*3.3/65535 #3.3 corresponde al voltaje de la Pico, 65535 corresponde a 2^16 -1 (numero de bits)
        c_temp= 27-(valor_raw-0.706)/0.001721 #Fórmula desde el datasheet
        far_temp=c_to_f(c_temp)
        k_temp=c_to_k(c_temp)
        
        cmd=input().strip().lower()
        if cmd=="celcius":
            print(f"La temperatura en Celcius es {c_temp}")
        elif cmd == "farenheit":
            print(f"La temperatura en Farenheit es {far_temp}")
        elif cmd == "kelvin":
            print(f"La temperatura en Kelvin es {k_temp}")
        elif cmd=="finalizar":
            print("El sistema se cerró")
            break
        else:
            print("Comando Incorrecto") 
        sleep(1)

if __name__ == "__main__":
    main()  # El uso de main es muy común en programas grandes, ya que permite controlar qué parte del código se ejecuta cuando el archivo es el programa principal.


