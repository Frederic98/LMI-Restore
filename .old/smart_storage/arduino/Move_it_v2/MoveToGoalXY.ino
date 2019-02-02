void MoveToGoalXY() {
  if (state != 4) Serial.println("starting movement");
  positions[0] = -stepsX;
  positions[1] = -stepsY;

  steppers.moveTo(positions);
  while ((stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) && state != 4) {
    steppers.run();
  }
  if (state != 4) Serial.println("steppers arrived at position");
}

