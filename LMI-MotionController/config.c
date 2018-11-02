#include "config.h"

uint8_t PINS_STEP[N_AXIS] = {12, 11, 10, 9};
uint8_t PINS_DIR[N_AXIS] = {7, 6, 13, 5};
uint8_t PINS_HOME[N_AXIS] = {2, 3, 18, 19};
uint32_t DEFAULT_SPEED[N_AXIS] = {500, 500, 3000, 400};
uint32_t MAX_SPEED[N_AXIS] = {500, 500, 3000, 400};
uint32_t MAX_ACCEL[N_AXIS] = {150, 150, 600, 100};
uint32_t STEPS_MM[N_AXIS] = {100, 100, 100, 100};
