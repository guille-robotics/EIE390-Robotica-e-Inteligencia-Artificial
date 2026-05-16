// Definición de pines para el motor A
const int motor1Pin1 = 26; // IN1 en el L298N
const int motor1Pin2 = 27; // IN2 en el L298N

void setup() {
  // Inicializamos los pines como salidas
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  
  // Nos aseguramos de que el motor empiece detenido
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
}

void loop() {
  // ----------------------------------------
  // 1. Mover hacia adelante
  // ----------------------------------------
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  delay(2000); // Gira por 2 segundos

  // ----------------------------------------
  // 2. Detener el motor
  // ----------------------------------------
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  delay(1000); // Se detiene por 1 segundo

  // ----------------------------------------
  // 3. Mover hacia atrás (Reversa)
  // ----------------------------------------
  // Invertimos los estados lógicos
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  delay(2000); // Gira en reversa por 2 segundos

  // ----------------------------------------
  // 4. Detener el motor
  // ----------------------------------------
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  delay(1000); // Se detiene por 1 segundo antes de repetir
}