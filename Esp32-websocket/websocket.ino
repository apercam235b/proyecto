#include <WiFi.h>
#include <WebSocketServer.h>

WiFiServer server(80);
WebSocketServer webSocketServer;

const char* ssid = "lowi54D0";
const char* password = "Jonnyessubnormal889";

void setup() {
  Serial.begin(115200);

  // Inicializar pines GPIO como entradas
  pinMode(16, INPUT);
  pinMode(17, INPUT);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to the WiFi network");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client && client.connected() && webSocketServer.handshake(client)) {
    Serial.println("Client connected");

    while (client.connected()) {
      String data = webSocketServer.getData();

      if (data.length() > 0) {
        Serial.println(data);

        // Leer el estado de los pines GPIO 16 y 17
        int pin16State = digitalRead(16);
        int pin17State = digitalRead(17);

        // Imprimir el estado de los pines en la consola
        Serial.print("Pin 16: ");
        Serial.println(pin16State);
        Serial.print("Pin 17: ");
        Serial.println(pin17State);

        // Enviar el estado de los pines al cliente
        String message = "Pin 16: " + String(pin16State) + " Pin 17: " + String(pin17State);
        webSocketServer.sendData(message);
      }

      delay(10); // Pequeño retraso para la recepción de datos
    }

    Serial.println("Client disconnected");
  }

  delay(100);
}

