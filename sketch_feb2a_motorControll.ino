#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
String command;
String previousCommand;
int angle = 0;
int x = 0;
int move;
int step;
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(100);
  // initialize the serial port:
  Serial.begin(9600);
}
void kick(){
    myStepper.step(stepsPerRevolution/4);
    myStepper.step(-stepsPerRevolution/2);
    myStepper.step(stepsPerRevolution/4);
}

void horizontal(){
  myStepper.step(stepsPerRevolution/4);
}

void clockwise(){
  myStepper.step(-stepsPerRevolution);
}

void anticlockwise(){
  myStepper.step(stepsPerRevolution);
}

void stand(){
  if (previousCommand.equals("horizontal")){
      myStepper.step(-stepsPerRevolution/4);
    }
}

void basePosition(){
  if(previousCommand.equals("horizontal") && !command.equals("stand")){
    myStepper.step(-stepsPerRevolution/4);
  }
}

void moveTo(int position){
  //11/22
  //want the max rotation to be 110 steps
  //so "position" is between 0 and 110
  if (position > 110 || position < 0){
    return;
  }
  if(position > x){
    //move in the positive direction
    step = position - x;
    myStepper.step(-step);
    x = position;
  }
  else if (position < x){
    //move in the negative direction
    step = x - position;
    myStepper.step(step);
    x = position;
  }
  else if (position == x){
    Serial.println("same position, no move");
    return;
  }
}

void fullIn(){
  moveTo(110);
}

void fullOut(){
  moveTo(0);
}

void printInt(int num){
  Serial.println(num);
}




// Main system loop
void loop() {
  if (Serial.available()){
    //to switch between lateral and player movement just comment and un-comment the two below lines alternately.
    command = Serial.readStringUntil('\n');
    //move = Serial.parseInt();
    command.trim();
    basePosition();

    if (command.equals("stand")){
        stand();
      }
    else if (command.equals("anticlockwise")){
        anticlockwise();
      }
    else if (command.equals("clockwise")){
        clockwise();
      }
    else if (command.equals("horizontal")){
        horizontal();
      }
    else if (command.equals("kick")){
        kick();
      }
    else{
      moveTo(move);

    }
    previousCommand = command;

  
}
}
  //Serial.println("counterclockwise");
  //myStepper.step(stepsPerRevolution);
  //delay(500);

  // step one revolution in the other direction:
  //Serial.println("clockwise");
  //myStepper.step(-stepsPerRevolution);
  //delay(500);
