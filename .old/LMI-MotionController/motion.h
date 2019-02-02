#ifndef MOTION_H
#define MOTION_H

#include <MultiStepper.h>
#include <AccelStepper.h>
#include "config.h"

extern uint32_t position[N_AXIS];
extern AccelStepper steppers[N_AXIS];
extern MultiStepper motion;

void setup_steppers();
uint32_t mmToSteps(uint8_t axis, float mm);
void setAxisFeedrate(uint32_t rate);
float stepsToMM(uint8_t axis, uint32_t steps);
uint32_t mmToSteps(uint8_t axis, float mm);
void home(bool x, bool y, bool z, bool r);

#endif //MOTION_H
