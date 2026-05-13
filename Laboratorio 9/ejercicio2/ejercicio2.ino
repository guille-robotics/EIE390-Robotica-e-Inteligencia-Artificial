#include <WiFi.h>
#include <WebServer.h>

// 1. CONFIGURACIÓN DE RED (¡Recuerde modificar esto por su grupo!)
const char *ssid = "ESP32_GrupoX";
const char *password = "12345678";

IPAddress local_IP(192, 168, 10, 1);
IPAddress gateway(192, 168, 10, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

// 2. CONFIGURACIÓN DE HARDWARE
const int ledPin = 2; // El pin 2 corresponde al LED azul integrado en la placa
bool estadoLED = false; // Variable para recordar si está encendido o apagado

// 3. FUNCIÓN PARA GENERAR LA INTERFAZ GRÁFICA (HTML + CSS básico)
String generarHTML() {
  String html = "<!DOCTYPE html><html><head>";
  html += "<meta charset='UTF-8'>";
  
  // Esta etiqueta asegura que la página se escale correctamente en la pantalla del celular
  html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"; 
  html += "<title>Control de LED</title>";
  
  // Estilos CSS para que los botones sean grandes y atractivos
  html += "<style>";
  html += "body { text-align: center; font-family: Arial; margin-top: 50px; }";
  html += "button { font-size: 20px; padding: 15px 30px; margin: 10px; border-radius: 8px; cursor: pointer; }";
  html += ".btn-on { background-color: #4CAF50; color: white; border: none; }"; // Verde
  html += ".btn-off { background-color: #f44336; color: white; border: none; }"; // Rojo
  html += "</style></head><body>";
  
  html += "<h1>Laboratorio EIE390</h1>";

  // Mostrar el estado actual en pantalla de forma dinámica
  if(estadoLED) {
    html += "<h2>Estado del actuador: <span style='color: green;'>ENCENDIDO</span></h2>";
  } else {
    html += "<h2>Estado del actuador: <span style='color: red;'>APAGADO</span></h2>";
  }

  // Creación de los botones HTML con sus respectivas rutas de destino
  html += "<button class='btn-on' onclick=\"window.location.href='/encender'\">Encender LED</button>";
  html += "<br>"; // Salto de línea entre botones
  html += "<button class='btn-off' onclick=\"window.location.href='/apagar'\">Apagar LED</button>";

  html += "</body></html>";
  return html;
}

// 4. FUNCIONES CONTROLADORAS DE LAS RUTAS (EndPoints)

// Función para la raíz (Cuando el alumno solo entra a la IP: 192.168.10.1)
void handleRoot() {
  server.send(200, "text/html", generarHTML());
}

// Función que se ejecuta cuando el alumno presiona el botón "Encender"
void handleEncender() {
  digitalWrite(ledPin, HIGH); // Acción física: Enviar 3.3V al pin
  estadoLED = true;           // Actualizar la variable lógica
  server.send(200, "text/html", generarHTML()); // Responder actualizando la web
}

// Función que se ejecuta cuando el alumno presiona el botón "Apagar"
void handleApagar() {
  digitalWrite(ledPin, LOW);  // Acción física: Enviar 0V al pin
  estadoLED = false;          // Actualizar la variable lógica
  server.send(200, "text/html", generarHTML()); // Responder actualizando la web
}

void setup() {
  Serial.begin(115200);
  
  // Configurar el pin del LED como salida e iniciar apagado
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Levantar red Wi-Fi
  Serial.println("\nConfigurando el Access Point...");
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.softAPIP());

  // Vincular las rutas de internet a las funciones de C++ correspondientes
  server.on("/", handleRoot);
  server.on("/encender", handleEncender);
  server.on("/apagar", handleApagar);

  // Arrancar el servidor web
  server.begin();
  Serial.println("Servidor HTTP iniciado.");
}

void loop() {
  // Escuchar permanentemente si algún celular se conecta y envía una petición
  server.handleClient();
}