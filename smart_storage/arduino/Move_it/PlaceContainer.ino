void PlaceContainer(){
  Serial.println("Placing container");

  Serial.println("Rotating Arm");
  stepperR.moveTo(Rconstant);

  while(stepperR.distanceToGo() != 0){
    stepperR.run();
  }

  Serial.println("Arm rotated");

  Serial.println("Extending Arm");

  stepperZ.moveTo(Zconstant);

  while(stepperZ.distanceToGo() != 0){
    stepperZ.run();
  }

  Serial.println("Arm extended");

  stepperY.moveTo(-Yconstant);

  while(stepperY.distanceToGo() != 0){
    stepperY.run();
  }

  Serial.println("Container unhooked");
  Serial.println("retracting");

  stepperZ.moveTo(0);

  while(stepperZ.distanceToGo() != 0){
    stepperZ.run();
  }

  Serial.println("Container placed");

  stepsX= 0;
  stepsY= 0;
  state = 1;
}


