#include "DHT.h"

#define DHTPIN 2     
#define DHTTYPE DHT11
#define LED_BLU 7
#define LED_ROSSO 11
#define LED_VERDE 9

DHT dht(DHTPIN, DHTTYPE);

unsigned long ultimoTempo = 0;
const unsigned long intervallo = 2000;

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  pinMode(LED_BLU, OUTPUT);
  pinMode(LED_ROSSO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
}

void loop() {
  if (millis() - ultimoTempo >= intervallo) {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (!isnan(h) && !isnan(t)) {
      
      if (t < 18) {
        digitalWrite(LED_BLU, HIGH); 
        digitalWrite(LED_VERDE, LOW);
        digitalWrite(LED_ROSSO, LOW);
      } 
      else if (t >= 18 && t <= 25) {
        digitalWrite(LED_BLU, LOW);
        digitalWrite(LED_VERDE, HIGH);
        digitalWrite(LED_ROSSO, LOW);
      } 
      else {
        digitalWrite(LED_BLU, LOW);
        digitalWrite(LED_VERDE, LOW);
        digitalWrite(LED_ROSSO, HIGH);
      }

      Serial.print(t);
      Serial.print(",");
      Serial.println(h);
    }

    ultimoTempo = millis();
  }
}