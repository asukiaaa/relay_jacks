#include <Arduino.h>
#include <MPU9250_asukiaaa.h>

const unsigned long minOnMillis = 1000;
const int OUTPUT_PINS[] = {A2, A0, A1, 16, 14, 15, 6, 5, 4};
const int OUTPUT_NUM = sizeof(OUTPUT_PINS);
unsigned long outputOnAt[OUTPUT_NUM];
MPU9250 sensor;

void setup() {
  // Serial.begin(9600);
  Wire.begin();
  sensor.setWire(&Wire);
  sensor.beginAccel();
  for(int i = 0; i < OUTPUT_NUM; ++i) {
    pinMode(OUTPUT_PINS[i], OUTPUT);
    outputOnAt[i] = 0;
  }
  delay(minOnMillis);
}

void setOutputLevel(int level) {
  // Serial.println(level);
  unsigned long currentMillis = millis();
  for (int i = 0; i < OUTPUT_NUM; ++i) {
    boolean power = i < level;
    if (power) {
      outputOnAt[i] = currentMillis;
    } else if (outputOnAt[i] + minOnMillis > currentMillis) {
      power = true;
    }
    digitalWrite(OUTPUT_PINS[i], power);
  }
}

int getLevelOfAccel() {
  float accelSum = sensor.accelSqrt();
  return (int) ((accelSum - 1.1) / 0.4);
}

void loop() {
  sensor.accelUpdate();
  setOutputLevel(getLevelOfAccel());
  delay(80);
}
