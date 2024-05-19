#include <WiFi.h>
#include <WebSocketServer.h>

WiFiServer server(80);
WebSocketServer webSocketServer;

const char* ssid = "lowi54D0";
const char* password = "Jonnyessubnormal889";

void setup() {
  Serial.begin(115200);

  // Inicializar pines GPIO
  pinMode(16, OUTPUT);
  pinMode(17, OUTPUT);

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
        webSocketServer.sendData(data);

        // Simulación del envío de datos por GPIO 16 y 17
        digitalWrite(16, HIGH);
        delay(500);  // Mantener el estado por un corto tiempo
        digitalWrite(16, LOW);
        digitalWrite(17, HIGH);
        delay(500);  // Mantener el estado por un corto tiempo
        digitalWrite(17, LOW);
      }

      delay(10); // Pequeño retraso para la recepción de datos
    }

    Serial.println("Client disconnected");
  }

  delay(100);
}
