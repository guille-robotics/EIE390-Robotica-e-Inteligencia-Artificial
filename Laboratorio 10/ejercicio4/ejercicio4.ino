#include <WiFi.h>
#include <WebServer.h>

// ==========================================
// 1. CONFIGURACIÓN DE RED 
// ==========================================
const char *ssid = "ESP32_GrupoX";
const char *password = "12345678";

IPAddress local_IP(192, 168, 10, 1);
IPAddress gateway(192, 168, 10, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

// ==========================================
// 2. CONFIGURACIÓN DE HARDWARE (MOTOR)
// ==========================================
const int motor1Pin1 = 26; // IN1
const int motor1Pin2 = 27; // IN2
const int enable1Pin = 14; // ENA (PWM)

// Configuración PWM (ESP32 v3.0+)
const int freq = 5000;
const int resolution = 8;
const int velocidad = 150; // Velocidad fija para los movimientos por web

// Variable para recordar el estado y mostrarlo en la página web
String estadoMotor = "DETENIDO"; 

// ==========================================
// 3. FUNCIÓN PARA GENERAR LA INTERFAZ WEB
// ==========================================
String generarHTML() {
  String html = "<!DOCTYPE html><html><head>";
  html += "<meta charset='UTF-8'>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"; 
  html += "<title>Control Inalámbrico Motor</title>";
  
  // Estilos CSS: Se añade un tercer botón y se ajustan colores
  html += "<style>";
  html += "body { text-align: center; font-family: Arial; margin-top: 40px; background-color: #f4f4f9;}";
  html += "button { font-size: 22px; padding: 15px; margin: 10px; border-radius: 8px; cursor: pointer; width: 80%; max-width: 300px; font-weight: bold; }";
  html += ".btn-fwd { background-color: #4CAF50; color: white; border: none; }"; // Verde
  html += ".btn-rev { background-color: #2196F3; color: white; border: none; }"; // Azul
  html += ".btn-stop { background-color: #f44336; color: white; border: none; }"; // Rojo
  html += "</style></head><body>";
  
  html += "<h1>Laboratorio EIE</h1>";

  // Mostrar el estado actual del motor
  html += "<h2>Estado: <strong>" + estadoMotor + "</strong></h2>";

  // Creación de los tres botones con sus rutas correspondientes
  html += "<button class='btn-fwd' onclick=\"window.location.href='/adelante'\">Girar Adelante</button><br>";
  html += "<button class='btn-stop' onclick=\"window.location.href='/detener'\">DETENER MOTOR</button><br>";
  html += "<button class='btn-rev' onclick=\"window.location.href='/atras'\">Girar Atrás</button>";

  html += "</body></html>";
  return html;
}

// ==========================================
// 4. FUNCIONES CONTROLADORAS DE RUTAS
// ==========================================

// Carga la página principal
void handleRoot() {
  server.send(200, "text/html", generarHTML());
}

// Ruta: /adelante
void handleAdelante() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  ledcWrite(enable1Pin, velocidad); // Activa el PWM
  estadoMotor = "ADELANTE";
  server.send(200, "text/html", generarHTML()); 
}

// Ruta: /atras
void handleAtras() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  ledcWrite(enable1Pin, velocidad); // Activa el PWM
  estadoMotor = "ATRÁS";
  server.send(200, "text/html", generarHTML()); 
}

// Ruta: /detener
void handleDetener() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  ledcWrite(enable1Pin, 0); // Apaga el PWM por seguridad
  estadoMotor = "DETENIDO";
  server.send(200, "text/html", generarHTML()); 
}

void setup() {
  Serial.begin(115200);
  
  // Configurar pines de control del motor como salida
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  
  // Configurar PWM del ESP32 v3.0+
  ledcAttach(enable1Pin, freq, resolution);

  // Asegurarnos de que el motor inicie detenido
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  ledcWrite(enable1Pin, 0);

  // Levantar red Wi-Fi (Access Point)
  Serial.println("\nConfigurando el Access Point...");
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.print("Red Wi-Fi creada. Conéctate a 'ESP32_GrupoX' y entra a la IP: ");
  Serial.println(WiFi.softAPIP());

  // Vincular las rutas de internet a las funciones
  server.on("/", handleRoot);
  server.on("/adelante", handleAdelante);
  server.on("/atras", handleAtras);
  server.on("/detener", handleDetener);

  // Arrancar el servidor web
  server.begin();
  Serial.println("Servidor HTTP iniciado.");
}

void loop() {
  // Escuchar peticiones entrantes de los clientes (celular, PC, etc.)
  server.handleClient();
}