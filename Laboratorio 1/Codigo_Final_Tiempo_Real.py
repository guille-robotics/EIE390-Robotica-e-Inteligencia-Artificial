from machine import ADC
from time import sleep
from src.funciones import c_to_f, c_to_k
import sys
import select


def main():
    sensor_temp = ADC(4)

    print("Medidor de Temperaturas")
    print("Comandos: celsius | fahrenheit | kelvin | finalizar")

    modo = None  # estado actual del sistema

    while True:
        # Leer temperatura
        valor_raw = sensor_temp.read_u16() * 3.3 / 65535
        c_temp = 27 - (valor_raw - 0.706) / 0.001721

        # Mostrar según el modo actual
        if modo == "celsius":
            print(f"temp_c = {round(c_temp, 2)}")

        elif modo == "fahrenheit":
            print(f"temp_f = {round(c_to_f(c_temp), 2)}")

        elif modo == "kelvin":
            print(f"temp_k = {round(c_to_k(c_temp), 2)}")

        sleep(1)

        # Revisa si el usuario ingresó un nuevo comando por teclado
        # sin detener el ciclo principal del programa
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:

            # Lee el comando escrito por el usuario
            # y lo normaliza para facilitar la comparación
            cmd = sys.stdin.readline().strip().lower()
            if cmd == "":
                continue

            if cmd == "finalizar":
                print("Sistema detenido")
                break
            elif cmd in ["celsius", "fahrenheit", "kelvin"]:
                modo = cmd
            else:
                print("Comando incorrecto")


if __name__ == "__main__":
    main()
