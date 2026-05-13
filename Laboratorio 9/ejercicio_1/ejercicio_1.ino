#include <WiFi.h>
#include <WebServer.h> // Libreria necesaria para levantar el servidor web

// 1. ASIGNE UN NOMBRE ÚNICO A SU RED
const char *ssid = "ESP32_GrupoX";
const char *password = "12345678"; 

// 2. CONFIGURE UNA IP ÚNICA 
IPAddress local_IP(192, 168, 10, 1);  // Direccion IP estatica
IPAddress gateway(192, 168, 10, 1);   // Puerta de enlace
IPAddress subnet(255, 255, 255, 0);   // Mascara de subred

// 3. CREAR EL OBJETO SERVIDOR EN EL PUERTO 80
WebServer server(80);

// Funcion que se ejecuta cuando un cliente entra a la IP
void handleRoot() {
  // Envia un codigo de exito (200), el tipo de contenido y el texto HTML
  server.send(200, "text/html", "<h1>Hola desde el ESP32!</h1><p>Conexion y servidor funcionando correctamente.</p>");
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("Configurando el Access Point...");

  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);

  Serial.print("Access Point Iniciado. SSID: ");
  Serial.println(ssid);
  Serial.print("Direccion IP del ESP32: ");
  Serial.println(WiFi.softAPIP());

  // 4. CONFIGURAR Y ARRANCAR EL SERVIDOR
  server.on("/", handleRoot); // Si entran a la raiz ("/"), ejecuta handleRoot
  server.begin();             // Inicia el servidor
  Serial.println("Servidor HTTP iniciado en el puerto 80.");
}

void loop() {
  // 5. ESCUCHAR CONSTANTEMENTE A LOS CLIENTES ENTRANTES
  server.handleClient();
}