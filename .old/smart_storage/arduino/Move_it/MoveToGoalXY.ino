void MoveToGoalXY(){
  Serial.println("starting movement");
  positions[0]= -stepsX;
  positions[1]= -stepsY;

  steppers.moveTo(positions);
  steppers.runSpeedToPosition();
  Serial.println("steppers arrived at position");  
}

