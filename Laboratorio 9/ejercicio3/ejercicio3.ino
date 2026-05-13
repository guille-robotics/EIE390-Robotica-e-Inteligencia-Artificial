#include <WiFi.h>
#include <WebServer.h>

// 1. CONFIGURACIÓN DE RED 
const char *ssid = "ESP32_GrupoX";
const char *password = "12345678";

IPAddress local_IP(192, 168, 10, 1);
IPAddress gateway(192, 168, 10, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

// 2. CONFIGURACIÓN DE HARDWARE
const int ledPin = 2;    // LED azul integrado
const int buzzerPin = 4; // Pin conectado al Buzzer

bool estadoLED = false;
bool estadoBuzzer = false;

// 3. FUNCIÓN PARA GENERAR LA INTERFAZ GRÁFICA (HTML + CSS)
String generarHTML() {
  String html = "<!DOCTYPE html><html><head>";
  html += "<meta charset='UTF-8'>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"; 
  html += "<title>Control de ESP32</title>";
  
  html += "<style>";
  html += "body { text-align: center; font-family: Arial; margin-top: 30px; }";
  html += "button { font-size: 18px; padding: 15px 30px; margin: 10px; border-radius: 8px; cursor: pointer; width: 80%; max-width: 300px;}";
  html += ".btn-on { background-color: #4CAF50; color: white; border: none; }"; 
  html += ".btn-off { background-color: #f44336; color: white; border: none; }"; 
  html += ".panel { border: 2px solid #ccc; padding: 15px; margin: 20px auto; width: 90%; max-width: 400px; border-radius: 10px; }";
  html += "</style></head><body>";
  
  html += "<h1>Panel de Control IoT</h1>";

  // Panel del LED
  html += "<div class='panel'>";
  html += "<h2>LED Integrado</h2>";
  if(estadoLED) {
    html += "<p>Estado: <span style='color: green; font-weight: bold;'>ENCENDIDO</span></p>";
  } else {
    html += "<p>Estado: <span style='color: red; font-weight: bold;'>APAGADO</span></p>";
  }
  html += "<button class='btn-on' onclick=\"window.location.href='/led_on'\">Encender LED</button><br>";
  html += "<button class='btn-off' onclick=\"window.location.href='/led_off'\">Apagar LED</button>";
  html += "</div>";

  // Panel del Buzzer
  html += "<div class='panel'>";
  html += "<h2>Buzzer Activo</h2>";
  if(estadoBuzzer) {
    html += "<p>Estado: <span style='color: green; font-weight: bold;'>SONANDO</span></p>";
  } else {
    html += "<p>Estado: <span style='color: red; font-weight: bold;'>SILENCIO</span></p>";
  }
  html += "<button class='btn-on' onclick=\"window.location.href='/buzzer_on'\">Encender Buzzer</button><br>";
  html += "<button class='btn-off' onclick=\"window.location.href='/buzzer_off'\">Apagar Buzzer</button>";
  html += "</div>";

  html += "</body></html>";
  return html;
}

// 4. FUNCIONES CONTROLADORAS DE LAS RUTAS

void handleRoot() {
  server.send(200, "text/html", generarHTML());
}

// Controladores para el LED
void handleLedOn() {
  digitalWrite(ledPin, HIGH);
  estadoLED = true;           
  server.send(200, "text/html", generarHTML()); 
}

void handleLedOff() {
  digitalWrite(ledPin, LOW);  
  estadoLED = false;          
  server.send(200, "text/html", generarHTML()); 
}

// Controladores para el Buzzer
void handleBuzzerOn() {
  digitalWrite(buzzerPin, HIGH);
  estadoBuzzer = true;           
  server.send(200, "text/html", generarHTML()); 
}

void handleBuzzerOff() {
  digitalWrite(buzzerPin, LOW);  
  estadoBuzzer = false;          
  server.send(200, "text/html", generarHTML()); 
}

void setup() {
  Serial.begin(115200);
  
  // Configurar pines
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  digitalWrite(ledPin, LOW);
  digitalWrite(buzzerPin, LOW);

  // Levantar red Wi-Fi
  Serial.println("\nConfigurando el Access Point...");
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.softAPIP());

  // Vincular las rutas
  server.on("/", handleRoot);
  server.on("/led_on", handleLedOn);
  server.on("/led_off", handleLedOff);
  server.on("/buzzer_on", handleBuzzerOn);
  server.on("/buzzer_off", handleBuzzerOff);

  // Arrancar el servidor
  server.begin();
  Serial.println("Servidor HTTP iniciado.");
}

void loop() {
  server.handleClient();
}