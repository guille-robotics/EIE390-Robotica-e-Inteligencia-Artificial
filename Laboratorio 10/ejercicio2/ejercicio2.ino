// Definición de pines para dirección y velocidad
const int motor1Pin1 = 26; 
const int motor1Pin2 = 27; 
const int enable1Pin = 14; // Pin ENA conectado al GPIO 14 (PWM)

// Propiedades de la señal PWM para el ESP32 (Nueva versión)
const int freq = 5000;        // Frecuencia de 5000 Hz
const int resolution = 8;     // Resolución de 8 bits (valores de 0 a 255)

void setup() {
  // Inicializamos los pines de dirección
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  
  // NUEVA FORMA: Configuramos el PWM y lo asignamos al pin en una sola línea
  ledcAttach(enable1Pin, freq, resolution);
}

void loop() {
  // Establecemos la dirección hacia adelante
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);

  // ----------------------------------------
  // Acelerar: Aumentamos el ciclo de trabajo de 0 a 255
  // ----------------------------------------
  for(int dutyCycle = 0; dutyCycle <= 255; dutyCycle++){   
    // NUEVA FORMA: ledcWrite ahora recibe el PIN directamente, no el canal
    ledcWrite(enable1Pin, dutyCycle);
    delay(15); 
  }

  // ----------------------------------------
  // Desacelerar: Reducimos el ciclo de trabajo de 255 a 0
  // ----------------------------------------
  for(int dutyCycle = 255; dutyCycle >= 0; dutyCycle--){
    ledcWrite(enable1Pin, dutyCycle);
    delay(15);
  }
  
  // Nos aseguramos de que el motor se detenga completamente
  ledcWrite(enable1Pin, 0);
  delay(1000); 
}