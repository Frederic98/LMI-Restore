void PlaceContainer() {
  if (state != 4) Serial.println("Placing container");

  if (state != 4) Serial.println("Rotating Arm");
  stepperR.moveTo(Rconstant);

  while (stepperR.distanceToGo() != 0 && state != 4) {
    stepperR.run();
  }

  if (state != 4) Serial.println("Arm rotated");

  if (state != 4) Serial.println("Extending Arm");

  stepperZ.moveTo(ZconstantP);

  while (stepperZ.distanceToGo() != 0 && state != 4) {
    stepperZ.run();
  }

  if (state != 4) Serial.println("Arm extended");

  stepperY.moveTo(-Yconstant);

  while (stepperY.distanceToGo() != 0 && state != 4) {
    stepperY.run();
  }

  if (state != 4) Serial.println("Container unhooked");
  if (state != 4) Serial.println("retracting");

  stepperZ.moveTo(0);

  while (stepperZ.distanceToGo() != 0 && state != 4) {
    stepperZ.run();
  }

  if (state != 4) Serial.println("Container placed");
  if (state != 4) {
    stepsX = -10;
    stepsY = -10;
    state = 1;
  }
}


