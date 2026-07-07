/*
  ============================================================
  Water Quality Monitoring - Sensor Node Firmware
  Board: ESP32 / ESP8266 (WiFi-enabled)
  Sensors: Analog pH probe, Turbidity sensor, TDS sensor
  Publishes readings over MQTT for downstream ingestion
  (see src/data_ingestion/mqtt_client.py)
  ============================================================
*/

#include <WiFi.h>
#include <PubSubClient.h>

// ---------- WiFi credentials ----------
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ---------- MQTT broker settings ----------
const char* MQTT_BROKER   = "broker.hivemq.com";
const int   MQTT_PORT     = 1883;
const char* MQTT_TOPIC    = "waterquality/sensors";
const char* MQTT_CLIENT_ID = "esp32-water-node-01";

// ---------- Sensor pins ----------
const int PH_PIN         = 34;  // Analog pin for pH probe
const int TURBIDITY_PIN  = 35;  // Analog pin for turbidity sensor
const int TDS_PIN        = 32;  // Analog pin for TDS sensor

// ---------- Calibration constants (adjust after calibrating your probes) ----------
const float PH_OFFSET       = 0.0;
const float PH_SLOPE        = 3.5;
const float TDS_VREF        = 3.3;
const float TDS_K           = 0.5;

const unsigned long PUBLISH_INTERVAL_MS = 5000; // publish every 5s

WiFiClient espClient;
PubSubClient mqttClient(espClient);
unsigned long lastPublish = 0;

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP: " + WiFi.localIP().toString());
}

void connectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (mqttClient.connect(MQTT_CLIENT_ID)) {
      Serial.println("connected.");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retrying in 3s");
      delay(3000);
    }
  }
}

float readPH() {
  int raw = analogRead(PH_PIN);
  float voltage = raw * (3.3 / 4095.0);
  return PH_SLOPE * voltage + PH_OFFSET;
}

float readTurbidityNTU() {
  int raw = analogRead(TURBIDITY_PIN);
  float voltage = raw * (3.3 / 4095.0);
  // Simple linear approximation; calibrate against known NTU standards
  float ntu = -1120.4 * (voltage * voltage) + 5742.3 * voltage - 4352.9;
  if (ntu < 0) ntu = 0;
  return ntu;
}

float readTDSppm() {
  int raw = analogRead(TDS_PIN);
  float voltage = raw * (TDS_VREF / 4095.0);
  float tds = (133.42 * voltage * voltage * voltage
               - 255.86 * voltage * voltage
               + 857.39 * voltage) * TDS_K;
  if (tds < 0) tds = 0;
  return tds;
}

void publishReading() {
  float ph = readPH();
  float turbidity = readTurbidityNTU();
  float tds = readTDSppm();

  String payload = "{";
  payload += "\"ph\":" + String(ph, 2) + ",";
  payload += "\"turbidity\":" + String(turbidity, 2) + ",";
  payload += "\"tds\":" + String(tds, 2) + ",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";

  mqttClient.publish(MQTT_TOPIC, payload.c_str());
  Serial.println("Published: " + payload);
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (!mqttClient.connected()) {
    connectMQTT();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;
    publishReading();
  }
}
