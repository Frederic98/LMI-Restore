#include "mbed.h"
#include "MotionPlanner.h"

DigitalOut xs(PE_2);
DigitalOut ys(PD_11);
DigitalOut zs(PD_13);
DigitalOut rs(PD_12);
DigitalOut xd(PB_2);
DigitalOut yd(PB_6);
DigitalOut zd(PC_2);
DigitalOut rd(PF_4);

DigitalOut ybrake(PF_8);

DigitalIn xlim1(PE_15);
DigitalIn xlim2(PE_14);
DigitalIn ylim1(PE_12);
DigitalIn ylim2(PE_10);
DigitalIn zlim1(PG_14);
DigitalIn rlim1(PE_8);
DigitalIn rlim2(PG_9);

MotionPlanner xaxis = MotionPlanner(TIM2, xs, false, xd, true);
MotionPlanner yaxis = MotionPlanner(TIM2, ys, false, yd, false);
MotionPlanner zaxis = MotionPlanner(TIM2, zs, false, zd, true);
MotionPlanner raxis = MotionPlanner(TIM2, rs, false, rd, true);

char buffer[256];
char gline[128];
unsigned int buffer_length;
char* gcode_buffer;
char* gcode_pointer;
Serial host(USBTX, USBRX, 115200);

DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalIn button(USER_BUTTON);

void process_gline(char * buffer);
void serial_rx();

int main()
{
    ybrake = 0;
    host.attach(&serial_rx);
    
    xaxis.set_limitswitch(xlim1, 0, false);
    xaxis.set_limitswitch(xlim2, 1, false);
    yaxis.set_limitswitch(ylim1, 0, false);
    yaxis.set_limitswitch(ylim2, 1, false);
    zaxis.set_limitswitch(zlim1, 0, false);
    raxis.set_limitswitch(rlim1, 0, false);
    raxis.set_limitswitch(rlim2, 1, false);
    
    printf("X limits: %d\n", xaxis.limit_count);
    printf("Y limits: %d\n", yaxis.limit_count);
    printf("Z limits: %d\n", zaxis.limit_count);
    printf("R limits: %d\n", raxis.limit_count);
    printf("Motion controller set up\n");
    
    __TIM2_CLK_ENABLE();
    MotionPlanner::initTimer(TIM2, TIM2_IRQn);
    xaxis.setAcceleration(1200);
    xaxis.setSpeed(2000);
    yaxis.setAcceleration(4800);
    yaxis.setSpeed(5000);
    zaxis.setAcceleration(3000);
    zaxis.setSpeed(20000);
    raxis.setAcceleration(3000);
    raxis.setSpeed(2000);
    __TIM2_CLK_ENABLE();
    
    wait(2);
    ybrake = 1;
    
    while (true) {
        char * gline_end = strchr(buffer, '\n');
        if(gline_end != NULL){
            *gline_end = '\0';
            strcpy(gline, buffer);
            process_gline(gline);
            buffer[0] = '\0';
            buffer_length = 0;
            printf("ok\n");
        }
    }
}

void serial_rx(){
    char c = host.getc();
    if(c == '\b'){
#ifdef ECHO_SERIAL
        printf("\b ");
#endif
        buffer_length--;
    }else{
        buffer[buffer_length++] = c;
    }
#ifdef ECHO_SERIAL
    printf("%c", c);
#endif
    buffer[buffer_length] = '\0';
}

bool gcode_seen(char c){
    gcode_pointer = gcode_buffer;
    do{
      // Keep searching for character until on of the following conditions is met:
      // - Character is at the start of the string
      // - Character is preceded by a whitespace
      // - The end of the stirng is reached
        gcode_pointer = strchr(gcode_pointer, c);
    }while(!(gcode_pointer == gcode_buffer || gcode_pointer == NULL || *(gcode_pointer-1) == ' '));
    return gcode_pointer != NULL;
}

long gcode_value(){
    return strtol(gcode_pointer+1, NULL, 0);
}

void process_gline(char* buffer){
    gcode_buffer = buffer;
    if(gcode_seen('G')){
        switch(gcode_value()){
            case 0:
            case 1:
                // G0 | G1: Linear move
                if(gcode_seen('X')) xaxis.prepareAbsoluteMove(gcode_value());
                if(gcode_seen('Y')) yaxis.prepareAbsoluteMove(gcode_value());
                if(gcode_seen('Z')) zaxis.prepareAbsoluteMove(gcode_value());
                if(gcode_seen('R')) raxis.prepareAbsoluteMove(gcode_value());
                xaxis.startMove();
                yaxis.startMove();
                zaxis.startMove();
                raxis.startMove();
                break;
            case 28:
                // G28: Home
                if(gcode_seen('X') || gcode_seen('Y') || gcode_seen('Z') || gcode_seen('R')){
                    if(gcode_seen('X')) xaxis.home(gcode_value());
                    if(gcode_seen('Y')) yaxis.home(gcode_value());
                    if(gcode_seen('Z')) zaxis.home(gcode_value());
                    if(gcode_seen('R')) raxis.home(gcode_value());
                }else{
                    xaxis.home();
                    yaxis.home();
                    zaxis.home();
                    raxis.home();
                }
                break;
            case 92:
                // G92: set current position
                if(gcode_seen('X')) xaxis.position = gcode_value();
                if(gcode_seen('Y')) yaxis.position = gcode_value();
                if(gcode_seen('Z')) zaxis.position = gcode_value();
                if(gcode_seen('R')) raxis.position = gcode_value();
                break;
        }
    }else if(gcode_seen('M')){
        switch(gcode_value()){
            case 200:
            //Set axis velocity
                if(gcode_seen('X')) xaxis.setSpeed(gcode_value());
                if(gcode_seen('Y')) yaxis.setSpeed(gcode_value());
                if(gcode_seen('Z')) zaxis.setSpeed(gcode_value());
                if(gcode_seen('R')) raxis.setSpeed(gcode_value());
                break;
            case 201:
            //Set axis acceleration
                if(gcode_seen('X')) xaxis.setAcceleration(gcode_value());
                if(gcode_seen('Y')) yaxis.setAcceleration(gcode_value());
                if(gcode_seen('Z')) zaxis.setAcceleration(gcode_value());
                if(gcode_seen('R')) raxis.setAcceleration(gcode_value());
                break;
            case 119:
            // Print limit switch state
                printf("Limits: ");
                printf("X(%c%c) ", xaxis.get_limitswitch_char(0), xaxis.get_limitswitch_char(1));
                printf("Y(%c%c) ", yaxis.get_limitswitch_char(0), yaxis.get_limitswitch_char(1));
                printf("Z(%c%c) ", zaxis.get_limitswitch_char(0), zaxis.get_limitswitch_char(1));
                printf("R(%c%c) ", raxis.get_limitswitch_char(0), raxis.get_limitswitch_char(1));
                break;
            case 400:
            // Wait for motion to finish
                if(gcode_seen('X') || gcode_seen('Y') || gcode_seen('Z') || gcode_seen('R')){
                    if(gcode_seen('X')) xaxis.wait();
                    if(gcode_seen('Y')) yaxis.wait();
                    if(gcode_seen('Z')) zaxis.wait();
                    if(gcode_seen('R')) raxis.wait();
                }else{
                    xaxis.wait();
                    yaxis.wait();
                    zaxis.wait();
                    raxis.wait();
                }
                break;
        }
    }
}