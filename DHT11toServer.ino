#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const char *ssid = "Fatlab";
const char *password = "12345678@!";
const char *mqtt_server = "192.168.1.148";

WiFiClient espClient;
PubSubClient client(espClient);

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");

  client.setServer(mqtt_server, 1884);
  dht.begin();
}

void loop() {
  // Đọc nhiệt độ và độ ẩm từ cảm biến DHT11
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  char tempString[10];
  char humString[10];

  dtostrf(temperature, 6, 2, tempString);
  dtostrf(humidity, 6, 2, humString);

  String tempTopic = "esp32/temperature";
  String humTopic = "esp32/humidity";

  String tempPayload = "{\"value\":" + String(tempString) + "}";
  String humPayload = "{\"value\":" + String(humString) + "}";

  if (client.connect("ESP32Client")) {
    client.publish(tempTopic.c_str(), tempPayload.c_str());
    client.publish(humTopic.c_str(), humPayload.c_str());
    client.disconnect();
  }

  delay(5000); // Gửi mỗi 5 giây
}
