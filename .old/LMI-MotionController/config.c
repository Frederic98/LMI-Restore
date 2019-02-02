#include "config.h"

//uint8_t PINS_STEP[N_AXIS] = {12, 11, 10, 9};
//uint8_t PINS_DIR[N_AXIS] = {7, 6, 13, 5};
//uint8_t PINS_HOME[N_AXIS] = {2, 3, 18, 19};
uint32_t DEFAULT_SPEED[N_AXIS] = {500000, 500000, 3000, 400};
uint32_t MAX_SPEED[N_AXIS] = {500000, 500000, 3000, 400};
uint32_t MAX_ACCEL[N_AXIS] = {5000, 5000, 600, 100};
uint32_t STEPS_MM[N_AXIS] = {100, 100, 100, 100};

uint8_t PINS_STEP[N_AXIS] = {25, 32, 35, 42};
uint8_t PINS_DIR[N_AXIS] = {23, 33, 36, 43};
#ifdef DRIVER_ENABLE
uint8_t PINS_ENA[N_AXIS] = {27, 31, 34, 37};
#endif
#ifdef DRIVER_CURRENT
uint8_t PINS_CURRENT[N_AXIS] = {44, 44, 45, 46};
#endif
