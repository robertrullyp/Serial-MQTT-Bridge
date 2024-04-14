#include <Adafruit_BMP280.h>
#include <ArduinoJson.h>

Adafruit_BMP280 bmp; // I2C

const int ledPin = PB9;  // Pin number of the BLUE LED
const int ledPin1 = PA14;  // Pin number of the RED LED

int ledState = LOW;  // ledState used to set the LED
int ledState1 = LOW;

unsigned long previousMillis = 0;  // will store last time LED was updated
unsigned long previousMillis1 = 0;

const long interval = 1000;  // interval at which to blink (milliseconds)
const long interval1 = 2000;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  if (!bmp.begin(0x76)) {
//    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
  unsigned long currentMillis = millis();
  unsigned long currentMillis1 = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    digitalWrite(ledPin, ledState);
  }
  if (currentMillis1 - previousMillis1 >= interval1) {
    previousMillis1 = currentMillis1;
    if (ledState1 == LOW) {
      ledState1 = HIGH;
    } else {
      ledState1 = LOW;
      sendjson();
    }
    digitalWrite(ledPin1, ledState1);
  }
}

void sendjson () {
  JsonDocument root;
  JsonObject pres = root.createNestedObject("Pressure");
  JsonObject alt = root.createNestedObject("Approx Altitude");
  JsonObject temp = root.createNestedObject("Temperature");

  pres["Value"] = bmp.readPressure();
  alt["Value"] = bmp.readAltitude(1008);  
  temp["Value"] = bmp.readTemperature();  
  pres["Unit"] = "Pa";
  alt["Unit"] = "M";  
  temp["Unit"] = "°C";  
  // JsonArray dt = pval.createNestedArray("dttt");
  // dt.add(123);
  
  serializeJson(root, Serial);
  //serializeJsonPretty(root, Serial);
}
