void grabbingAction(){

if (state != 4) Serial.println("Starting rotation");

stepperR.moveTo(Rconstant);

while (stepperR.distanceToGo() != 0 && state != 4) {
  stepperR.run();
}



stepperZ.moveTo(ZconstantG);


while (stepperZ.distanceToGo() != 0  && state != 4) {
  stepperZ.run();
}

positions[1] = -stepsY - Yconstant - 6;

stepperY.moveTo(positions[1]);
while (stepperY.distanceToGo() != 0 && state != 4) {
  stepperY.run();
}




if (state != 4) Serial.println("retracting");

stepperZ.moveTo(500);

while (stepperZ.distanceToGo() != 0 && state != 4) {
  stepperZ.run();
}

stepperR.moveTo(straight);

while (stepperR.distanceToGo() != 0 && state != 4) {
  stepperR.run();
}


if (state != 4) Serial.println("Container picked up from AGV");

}
