from machine import Pin, PWM
from time import sleep

# Configuración del Buzzer en GP0
buzzer = PWM(Pin(0))

# Diccionario de frecuencias de notas musicales (Hz)
NOTE_C4 = 262
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_G4 = 392
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_G5 = 784
NOTE_A5 = 880

def play_tone(frequency, duration):
    if frequency == 0:
        buzzer.duty_u16(0)  # Silencio
    else:
        buzzer.freq(frequency)
        buzzer.duty_u16(32768) # 50% volumen
    sleep(duration)
    buzzer.duty_u16(0)
    sleep(0.05) # Pausa pequeña entre notas

def play_mario():
    print("Reproduciendo: Super Mario Bros")
    melody = [
        (NOTE_E5, 0.15), (NOTE_E5, 0.15), (0, 0.15), (NOTE_E5, 0.15), 
        (0, 0.15), (NOTE_C5, 0.15), (NOTE_E5, 0.15), (0, 0.15), 
        (NOTE_G5, 0.15), (0, 0.3), (NOTE_G4, 0.15)
    ]
    for note, duration in melody:
        play_tone(note, duration)

def play_starwars():
    print("Reproduciendo: Star Wars Theme")
    melody = [
        (NOTE_D4, 0.2), (NOTE_D4, 0.2), (NOTE_D4, 0.2), 
        (NOTE_G4, 0.6), (NOTE_D5, 0.6), 
        (NOTE_C5, 0.15), (NOTE_B4, 0.15), (NOTE_A4, 0.15), (NOTE_G5, 0.6), (NOTE_D5, 0.3),
        (NOTE_C5, 0.15), (NOTE_B4, 0.15), (NOTE_A4, 0.15), (NOTE_G5, 0.6), (NOTE_D5, 0.3),
        (NOTE_C5, 0.15), (NOTE_B4, 0.15), (NOTE_C5, 0.15), (NOTE_A4, 0.6)
    ]
    for note, duration in melody:
        play_tone(note, duration)

def play_imperial():
    print("Reproduciendo: Imperial March")
    melody = [
        (NOTE_A4, 0.5), (NOTE_A4, 0.5), (NOTE_A4, 0.5), (NOTE_F4, 0.35), (NOTE_C5, 0.15),
        (NOTE_A4, 0.5), (NOTE_F4, 0.35), (NOTE_C5, 0.15), (NOTE_A4, 0.65)
    ]
    for note, duration in melody:
        play_tone(note, duration)

# Bucle principal de interacción por terminal
print("--- JUKEBOX RPI PICO ---")
print("Comandos disponibles: mario, starwars, imperial, salir")

try:
    while True:
        comando = input("\nIngresa el nombre de la canción: ").strip().lower()
        
        if comando == "mario":
            play_mario()
        elif comando == "starwars":
            play_starwars()
        elif comando == "imperial":
            play_imperial()
        elif comando == "salir":
            print("¡Adiós!")
            break
        else:
            print("Comando no reconocido. Intenta con: mario, starwars o imperial.")

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    print("\nPrograma finalizado.")