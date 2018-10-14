#include <MultiStepper.h>
#include <AccelStepper.h>

// EG X-Y position bed driven by 2 steppers
// Alas its not possible to build an array of these with different pins for each :-(

AccelStepper stepperX(AccelStepper::DRIVER, 12, 7);
AccelStepper stepperY(AccelStepper::DRIVER, 11, 6);
AccelStepper stepperZ(AccelStepper::DRIVER, 10, 12);
AccelStepper stepperR(AccelStepper::DRIVER, 9, 5);
// Up to 10 steppers can be handled as a group by MultiStepper
MultiStepper steppers;

#define switch_hX 2 // Pin 2 connected to Home Switch (MicroSwitch)
#define switch_hY 3 // Pin 3 connected to Home Switch (MicroSwitch)
#define switch_hZ 19 // Pin 19 connected to Home Switch (MicroSwitch)
#define switch_hR 20 // Pin 20 connected to Home Switch (MicroSwitch)
#define switch_I 21 // Pin 21 connected to Home Switch (MicroSwitch)

// Communication variables
char StartChar = 'a';
char EndChar = 'a';

// movement variables and constants
long Row;
long column;
long stepsY;
long stepsX;
long columndistance = 350;     // Amount of y steps between the containers
long Rowdistance = 470;      // Amount of x steps between the containers
long Zconstant = 5000;           // Amount of steps to reach the containers
long Yconstant = 200;       // amount of steps for grabbing the container
long Rconstant = 5000;     // amount of steps to rotate the container 180 degrees


bool Homing_status = false;
long initial_homingX = -1;
long initial_homingY = -1;
long initial_homingZ = -1;
long initial_homingR = -1;
long positions[2]; // 0=X 1=Y
int state = 1;
void setup() {
  Serial.begin(9600);
  // Configure each stepper
  stepperX.setMaxSpeed(175);   //1000
  stepperX.setAcceleration(50); //200
  stepperY.setMaxSpeed(100); //1000
  stepperY.setAcceleration(50); //50
  stepperZ.setMaxSpeed(300);  //3000
  stepperZ.setAcceleration(100); //3000 
  stepperR.setMaxSpeed(200); //3000
  stepperR.setAcceleration(100); //3000


  // Then give them to MultiStepper to manage
  steppers.addStepper(stepperX);
  steppers.addStepper(stepperY);
  Home();
}
void loop() {
  switch (state) {
  case 1:
    CommandMessage();

    break;
  case 2:                 // "Get" state (Get Box)
    //Home();                //Home axis
    ConvertToSteps();     // Calculate the position of the container
    MoveToGoalXY();       // Move to the container
    

    //GrabContainer();      // Grab the container
    MoveToGoalXY();         // Go to the placing position
    //PlaceContainer();     // Place the container
    Serial.println("Complete");
    state = 1;
    break;

  case 3:               // "Set" state (Place box)
    //Home();                //Home axis
    ConvertToSteps();     // Calculate the position of the container
    MoveToGoalXY();       // Move to the container
    //GrabContainer();      // Grab the container

    MoveToGoalXY();         // Go to the placing position
    //PlaceContainer();     // Place the container
    Serial.println("Complete");
    state = 1;
    break;


  default:
    Home();
    break;
  }
}

