#include <Arduino.h>
#include "motion.h"
#include "config.h"
//#include <stdlib.h>

char serialBuffer[128];
uint8_t serialBufferPos = 0;
char * codePointer;

bool code_seen(char c){
  codePointer = strchr(serialBuffer, c);
  return codePointer != NULL;
}

long code_value(){
  return strtol(codePointer+1, NULL, 0);
}

long code_value_float(){
  return strtod(codePointer+1, NULL);
}

long code_value_steps(uint8_t axis){
  return mmToSteps(axis, code_value_float());
}

void process_line(){
  if(code_seen('G')){
    switch(code_value()){
      case 0:
      case 1:
        // G0 | G1: Linear move
        if(code_seen('X')) position[X_AXIS] = code_value_steps(X_AXIS);
        if(code_seen('Y')) position[Y_AXIS] = code_value_steps(Y_AXIS);
        if(code_seen('Z')) position[Z_AXIS] = code_value_steps(Z_AXIS);
        if(code_seen('R')) position[R_AXIS] = code_value_steps(R_AXIS);
//        if(code_seen('F')) 
        motion.moveTo(position);
        motion.runSpeedToPosition();                            // Blocking...
        break;
      case 28:
        // G28: Home
        bool x = code_seen('X');
        bool y = code_seen('Y');
        bool z = code_seen('Z');
        bool r = code_seen('R');
        if(!(x | y | z | r)){
          // No axis specified, home all
          home(true, true, true, true);
        }else{
          // Home specified axes
          home(x, y, z, r);
        }
        break;
      case 92:
        // G92: set current position
        if(code_seen('X')) steppers[X_AXIS].setCurrentPosition(code_value_steps(X_AXIS));
        if(code_seen('Y')) steppers[Y_AXIS].setCurrentPosition(code_value_steps(Y_AXIS));
        if(code_seen('Z')) steppers[Z_AXIS].setCurrentPosition(code_value_steps(Z_AXIS));
        if(code_seen('R')) steppers[R_AXIS].setCurrentPosition(code_value_steps(R_AXIS));
    }
  }
}

void serialEvent(){
  while(Serial.available()){
    char c = Serial.read();
    if(c == '\n'){
      serialBuffer[serialBufferPos] = 0;      // Terminate string with null characer
      process_line();                         // Process the gcode line
      serialBufferPos = 0;                    // Reset buffer position
    }else{
      serialBuffer[serialBufferPos] = c;      // Add character to buffer
      serialBufferPos++;                      // Step to next position in buffer
    }
  }
}
