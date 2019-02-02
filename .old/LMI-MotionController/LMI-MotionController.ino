#include <MultiStepper.h>
#include <AccelStepper.h>
#include "config.h"
#include "motion.h"


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(2^30);
  Serial.println("LMI MotionController");
  
  setup_steppers();
#ifdef PIN_RELAY
  pinMode(PIN_RELAY, OUTPUT);
  digitalWrite(PIN_RELAY, HIGH);
#endif

  Serial.println("Setup done...");
  // home all axis
}

void loop() {
//  digitalWrite(PINS_STEP[0], HIGH);
//  digitalWrite(PINS_STEP[1], HIGH);
//  delay(1);
//  digitalWrite(PINS_STEP[0], LOW);
//  digitalWrite(PINS_STEP[1], LOW);
//  delay(1);
  Serial.println("loop");
  steppers[0].runToNewPosition(0);
  steppers[0].runToNewPosition(100000);
//  position[0] = 1000;
//  position[1] = 1000;
//  motion.moveTo(position);
//  motion.run(); // Blocks until all are in position
//  delay(1000);
//
//  position[0] = -1000;
//  position[1] = -1000;
//  motion.moveTo(position);
//  motion.run(); // Blocks until all are in position
//  delay(1000);
}
