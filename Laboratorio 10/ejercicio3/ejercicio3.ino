// ==========================================
// CONTROL DE MOTOR Y LECTURA DE ENCODER (A y B)
// ESP32 (Core v3.0+) + L298N
// ==========================================

// --- DEFINICIÓN DE PINES ---
// Pines para dirección y velocidad del motor (L298N)
const int motor1Pin1 = 26; 
const int motor1Pin2 = 27; 
const int enable1Pin = 14; // Pin PWM (Conectado a ENA sin jumper)

// Pines del Encoder de Cuadratura
const int encoderPinA = 32; 
const int encoderPinB = 33; 

// --- CONFIGURACIÓN DE VELOCIDAD (PWM) ---
const int freq = 5000;
const int resolution = 8;
// Velocidad del motor (0 a 255). 
// Recomendación: Ponla en 0 si quieres girar la rueda con la mano para ver bien las ondas.
const int velocidad = 150; 

// --- VARIABLE DEL ENCODER ---
// Aunque en este código graficaremos los estados puros, mantenemos 
// el contador funcionando en segundo plano por la interrupción.
volatile long encoderCount = 0;

// --- FUNCIÓN DE INTERRUPCIÓN (ISR) ---
// Se ejecuta automáticamente cada vez que el Canal A pasa de LOW a HIGH
void IRAM_ATTR readEncoder() {
  int estadoB = digitalRead(encoderPinB);
  if (estadoB > 0) {
    encoderCount++; // Gira hacia adelante
  } else {
    encoderCount--; // Gira hacia atrás
  }
}

void setup() {
  // Iniciamos comunicación a alta velocidad para gráficos fluidos en el Plotter
  Serial.begin(115200);

  // Configuración de pines de dirección del motor
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  
  // Configuración del PWM para la velocidad (Sintaxis ESP32 v3.0+)
  ledcAttach(enable1Pin, freq, resolution);

  // Configuración de pines del encoder
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);
  
  // Activamos la interrupción en el pin A
  attachInterrupt(digitalPinToInterrupt(encoderPinA), readEncoder, RISING);
}

void loop() {
  // ----------------------------------------------------
  // 1. MOVER HACIA ADELANTE DURANTE 10 SEGUNDOS
  // ----------------------------------------------------
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  ledcWrite(enable1Pin, velocidad);
  
  // Guardamos el tiempo en el que empezamos este movimiento
  unsigned long tiempoInicio = millis();
  
  // Mientras no hayan pasado 10,000 ms (10 seg), graficamos
  while (millis() - tiempoInicio < 10000) {
    // Leemos los estados lógicos actuales (0 o 1)
    int estadoA = digitalRead(encoderPinA);
    int estadoB = digitalRead(encoderPinB);

    // Formato para el Serial Plotter: "Canal_A, Canal_B"
    Serial.print(estadoA);
    Serial.print(","); 
    
    // Sumamos 2 al estado B para desplazarlo hacia arriba en la gráfica
    // Así las líneas no se dibujan una encima de la otra.
    Serial.println(estadoB + 2); 

    // Pausa muy corta (5ms) para no perder los pulsos si el motor gira rápido
    delay(5); 
  }

  // ----------------------------------------------------
  // 2. MOVER HACIA ATRÁS DURANTE 10 SEGUNDOS
  // ----------------------------------------------------
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  ledcWrite(enable1Pin, velocidad);
  
  // Reiniciamos el cronómetro para el nuevo movimiento
  tiempoInicio = millis();
  
  // Repetimos el ciclo de medición mientras retrocede
  while (millis() - tiempoInicio < 10000) { 
    int estadoA = digitalRead(encoderPinA);
    int estadoB = digitalRead(encoderPinB);

    Serial.print(estadoA);
    Serial.print(","); 
    Serial.println(estadoB + 2); 
    
    delay(5);
  }
}