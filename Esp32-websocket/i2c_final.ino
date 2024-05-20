#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <DFRobot_DF2301Q.h>

// I2C communication
DFRobot_DF2301Q_I2C DF2301Q;

const char* ssid = "lowi54D0";
const char* password = "Jonnyessubnormal889";

IPAddress local_IP(172, 24, 1, 200);
IPAddress gateway(172, 24, 1, 1);
IPAddress subnet(255, 255, 255, 0);

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

// Function to handle WebSocket events
void onWebSocketEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len) {
  switch (type) {
    case WS_EVT_CONNECT:
      Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
      client->text("Connected to WebSocket server");
      break;
    case WS_EVT_DISCONNECT:
      Serial.printf("WebSocket client #%u disconnected\n", client->id());
      break;
    case WS_EVT_DATA:
      Serial.printf("Data received from client #%u: %s\n", client->id(), data);
      // Handle incoming messages here
      break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
  }
}

void setup() {
  Serial.begin(115200);

  // Configure the static IP address
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }

  // Initialize the WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  // Initialize the WebSocket server
  ws.onEvent(onWebSocketEvent);
  server.addHandler(&ws);
  
  // Start the server
  server.begin();
  Serial.println("WebSocket server started");

  // Initialize the sensor
  while( !( DF2301Q.begin() ) ) {
    Serial.println("Communication with device failed, please check connection");
    delay(3000);
  }
  Serial.println("Begin ok!");

  // Set the voice volume
  DF2301Q.setVolume(7);
  Serial.println("Volume set to 7");

  // Set the wake-up duration
  DF2301Q.setWakeTime(15);
  Serial.println("Wake-up time set to 15");

  // Get the wake-up duration
  uint8_t wakeTime = DF2301Q.getWakeTime();
  Serial.print("wakeTime = ");
  Serial.println(wakeTime);
}

void loop() {
  // Get CMDID from the sensor
  uint8_t CMDID = DF2301Q.getCMDID();
  
  if (0 != CMDID) {
    Serial.print("CMDID = ");
    Serial.println(CMDID);
    
    // Broadcast the CMDID to all connected WebSocket clients
    String message = "CMDID: " + String(CMDID);
    ws.textAll(message);
  }

  // Add a small delay to avoid spamming the I2C bus
  delay(100);
}
