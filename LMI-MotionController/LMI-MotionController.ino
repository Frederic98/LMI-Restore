#include <MultiStepper.h>
#include <AccelStepper.h>
#include "config.h"
#include "motion.h"


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(2^30);

  setup_steppers();
  
  digitalWrite(PIN_RELAY, LOW);

  // home all axis
}

void loop() {
  
}
