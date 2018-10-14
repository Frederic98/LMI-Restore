void handingAction(){

if (state != 4) Serial.println("Starting rotation");

stepperR.moveTo(Rconstant);

while (stepperR.distanceToGo() != 0 && state != 4) {
  stepperR.run();
}

positions[1] = -stepsY - Yconstant;

stepperY.moveTo(positions[1]);
while (stepperY.distanceToGo() != 0 && state != 4) {
  stepperY.run();
}

stepperZ.moveTo(ZconstantP);


while (stepperZ.distanceToGo() != 0  && state != 4) {
  stepperZ.run();
}



if (state != 4)  Serial.println("Placing container on AGV");

positions[1] = -stepsY;

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


if (state != 4) Serial.println("Container placed on AGV");

}
