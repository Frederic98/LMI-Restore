#ifndef CONFIG_H
#define CONFIG_H
#include "Arduino.h"

#define N_AXIS 4

#define X_AXIS 0
#define Y_AXIS 1
#define Z_AXIS 2
#define R_AXIS 3

extern uint8_t PINS_STEP[N_AXIS];
extern uint8_t PINS_DIR[N_AXIS];
extern uint8_t PINS_HOME[N_AXIS];
#define DRIVER_ENABLE
#ifdef DRIVER_ENABLE
extern uint8_t PINS_ENA[N_AXIS];
#endif
extern uint32_t MAX_SPEED[N_AXIS];
extern uint32_t MAX_ACCEL[N_AXIS];
extern uint32_t MAX_POS[N_AXIS];
extern uint32_t STEPS_MM[N_AXIS];
extern uint32_t DEFAULT_SPEED[N_AXIS];

#define DRIVER_CURRENT
#ifdef DRIVER_CURRENT
extern uint8_t PINS_CURRENT[N_AXIS];
#endif

//#define PIN_RELAY 40
#define PIN_RELAY 24

#endif //CONFIG_H
