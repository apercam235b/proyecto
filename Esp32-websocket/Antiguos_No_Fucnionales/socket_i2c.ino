#include <WiFi.h>
#include <WebSocketServer.h>
#include <Wire.h>

// WiFi and WebSocket server setup
WiFiServer server(80);
WebSocketServer webSocketServer;

const char* ssid = "lowi54D0";
const char* password = "Jonnyessubnormal889";

// I2C setup using predefined constants SDA and SCL
TwoWire MyI2C = TwoWire(0);

void setup() {
  Serial.begin(115200);

  // Initialize I2C bus
  MyI2C.begin(SDA, SCL, 400000); // 400kHz frequency

  // Initialize WiFi
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

        // Read data from I2C bus
        int i2cData = readI2CData(MyI2C, 0x48); // Replace 0x48 with your I2C device address

        // Print the data read from I2C bus
        Serial.print("I2C Data: ");
        Serial.println(i2cData);

        // Send the data to the WebSocket client
        String message = "I2C Data: " + String(i2cData);
        webSocketServer.sendData(message);
      }

      delay(10); // Small delay for data reception
    }

    Serial.println("Client disconnected");
  }

  delay(100);
}

int readI2CData(TwoWire &i2cBus, uint8_t address) {
  i2cBus.beginTransmission(address);
  i2cBus.write(0); // Adjust this based on your sensor's register or command
  i2cBus.endTransmission();
  
  i2cBus.requestFrom(static_cast<uint8_t>(address), static_cast<uint8_t>(2)); // Request 2 bytes from the I2C device
  if (i2cBus.available()) {
    int data = i2cBus.read();
    data = (data << 8) | i2cBus.read(); // Combine two bytes into an integer
    return data;
  } else {
    Serial.println("I2C data not available");
    return -1; // Return an error value if no data is available
  }
}
