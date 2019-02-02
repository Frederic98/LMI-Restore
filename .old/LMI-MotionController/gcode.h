#ifndef GCODE_H
#define GCODE_H

void process_line();
bool code_seen(char c);
long code_value();
//void serialEvent();

#endif //GCODE_H
