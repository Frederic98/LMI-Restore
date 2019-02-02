void Home() {
  
  

  Homing_status = true;

  //Serial.println("DEBUG: Been here, done that. Gonna check Z.");

  //Home the Z
  while (!digitalRead(switch_hZ) && state != 4) {  // Make the Stepper move CCW until the switch is activated
    stepperZ.moveTo(initial_homingZ);  // Set the position to move to
    initial_homingZ--;  // Decrease by 1 for next move if needed
    stepperZ.run();  // Start moving the stepper
    delay(2);
  }
  //Serial.print("Z distance:");
    //Serial.println(initial_homingZ);


  //Serial.println("DEBUG: Been here, done that. Z-axis. Gonna check X");

  //Home the X
  while (!digitalRead(switch_hX) && state != 4) {  // Make the Stepper move CCW until the switch is activated
    stepperX.moveTo(initial_homingX);  // Set the position to move to
    initial_homingX++;  // Decrease by 1 for next move if needed
    stepperX.run();  // Start moving the stepper
    delay(5);
  }
  //Serial.print("X distance:");
    //Serial.println(initial_homingX);

  //Serial.println("DEBUG: Been here, done that. X-axis. Gonna check Y.");

  //Home the Y
  while (!digitalRead(switch_hY) && state != 4) {
    stepperY.moveTo(initial_homingY);  // Set the position to move to
    initial_homingY++;  // Decrease by 1 for next move if needed
    stepperY.run();  // Start moving the stepper
    delay(5);
  }
  
    //Serial.print("Y distance:");
    //Serial.println(initial_homingY);

  //Serial.println("DEBUG: Been here, done that. Y-axis. Gonna check R.");

  //Home the R
  while (!digitalRead(switch_hR)  && state != 4) {
    stepperR.moveTo(initial_homingR);  // Set the position to move to
    initial_homingR--;  // Decrease by 1 for next move if needed
    stepperR.run();  // Start moving the stepper
    delay(2);
  }
  
      //Serial.print("R distance:");
    //Serial.println(initial_homingR);


 // Serial.println("DEBUG: Been here, done that. R-axis");
  stepperZ.setCurrentPosition(0);
  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
  stepperR.setCurrentPosition(0);
  
    stepperR.moveTo(straight);
  
  while(stepperR.distanceToGo() != 0 && state != 4){
    stepperR.run();
  }
  
  
  stepperZ.moveTo(2000);
  
  while(stepperZ.distanceToGo() != 0 && state != 4){
    stepperZ.run();
  }
  

    positions[0] = -100;
  positions[1] = -100;

  steppers.moveTo(positions);
  while ((stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) && state != 4) {
    steppers.run();
  }
  
  
  if (state == 4) Serial.println("Error state");
  delay(1000);
  
  Homing_status = false;
}









