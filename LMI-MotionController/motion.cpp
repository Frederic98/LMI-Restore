#include "Arduino.h"
#include "config.h"
#include "motion.h"

uint32_t position[N_AXIS];
AccelStepper steppers[N_AXIS];
MultiStepper motion;

void setup_steppers(){
  for(uint8_t i=0; i<N_AXIS; i++){
    AccelStepper stepper(AccelStepper::DRIVER, PINS_STEP[i], PINS_DIR[i]);
    stepper.setMaxSpeed(MAX_SPEED[i]);
    stepper.setAcceleration(MAX_ACCEL[i]);
    stepper.setSpeed(DEFAULT_SPEED[i]);
    stepper.setMinPulseWidth(20);
    steppers[i] = stepper;
    motion.addStepper(stepper);
//#ifdef DRIVER_ENABLE
    pinMode(PINS_ENA[i], OUTPUT);
    digitalWrite(PINS_ENA[i], LOW);
//#endif
//#ifdef DRIVER_CURRENT
    analogWrite(PINS_CURRENT[i], 100);
//#endif
    //attachInterrupt(digitalPinToInterrupt(PINS_HOME[i]), limitSwitch, RISING);
  }
}

void setAxisFeedrate(uint32_t rate){
  int32_t dpsq[N_AXIS];
}

void home(bool x, bool y, bool z, bool r){
  // ToDo: Perform an actual homeing cycle...
  for(uint8_t i=0; i<N_AXIS; i++){
    position[i] = 0;
  }
  motion.moveTo(position);
}

float stepsToMM(uint8_t axis, uint32_t steps){
  return float(steps) / STEPS_MM[axis];
}

uint32_t mmToSteps(uint8_t axis, float mm){
  return mm * STEPS_MM[axis];
}
