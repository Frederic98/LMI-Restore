void GrabContainer(){
  if (state != 4) Serial.println("Grabbing container");
  if (state != 4) Serial.println("Extending Arm");

  stepperZ.moveTo(ZconstantG);

  while(stepperZ.distanceToGo() != 0  && state != 4){
    stepperZ.run();
  }

  if (state != 4) Serial.println("Container reached");
  if (state != 4) Serial.println("Hooking container");
  positions[0] = -stepsX;
  positions[1] = -stepsY-Yconstant;

  steppers.moveTo(positions);
  while ((stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) && state != 4) {
    steppers.run();
  }


 // stepperY.moveTo(stepsY+Yconstant);

 // while(stepperY.distanceToGo() != 0 && state != 4){
  //  stepperY.run();
 // }

  if (state != 4) Serial.println("Container hooked");
  if (state != 4) Serial.println("retracting");

  stepperZ.moveTo(500);

  while(stepperZ.distanceToGo() != 0 && state != 4){
    stepperZ.run();
  }

  if (state != 4) Serial.println("Container grabbed");
 
}


