void MoveToGoalXY() {
  if (state != 4) Serial.println("starting movement");
  positions[0] = -stepsX;
  positions[1] = -stepsY;




  
  stepperY.moveTo(positions[1]);

   while(stepperY.distanceToGo() != 0  && state != 4){
      stepperY.run();
    }
    
      stepperX.moveTo(positions[0]);

   while(stepperX.distanceToGo() != 0  && state != 4){
      stepperX.run();
    }

  if (state != 4) Serial.println("steppers arrived at position");
}

