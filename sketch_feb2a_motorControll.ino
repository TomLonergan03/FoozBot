#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
String command;
String previousCommand;
int angle = 0;
int x = 0; //x is the lateral position of the motor
int move;
int step;
String mode;
String inputline;
String movetype;
bool isInt = true;
int rotation;
// for your motor

// initialize the stepper libraries for both motors.
Stepper lateralStepper(stepsPerRevolution, 8, 9, 10, 11);
Stepper playerStepper(stepsPerRevolution,2,3,4,5);

void setup() {
  // set the speed at 60 rpm:
  lateralStepper.setSpeed(40);
  playerStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);
}
void kick(){
    playerStepper.step(stepsPerRevolution/4);
    playerStepper.step(-stepsPerRevolution/2);
    playerStepper.step(stepsPerRevolution/4);
}

void horizontal(){
  playerStepper.step(stepsPerRevolution/4);
}

void clockwise(){
  playerStepper.step(-stepsPerRevolution);
}

void anticlockwise(){
  playerStepper.step(stepsPerRevolution);
}

void stand(){
  if (previousCommand.equals("horizontal")){
      playerStepper.step(-stepsPerRevolution/4);
    }
}

void basePosition(){
  if(previousCommand.equals("horizontal") && !command.equals("stand")){
    playerStepper.step(-stepsPerRevolution/4);
  }
}

void resetLateral(){
  lateralStepper.step(-1.5*stepsPerRevolution);
  x = 110;
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
    lateralStepper.step(-step);
    x = position;
  }
  else if (position < x){
    //move in the negative direction
    step = x - position;
    lateralStepper.step(step);
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
  //playerStepper.step(stepsPerRevolution/4);
  if (Serial.available()){
    //reset the player position
    basePosition();
    //read the input
    inputline = Serial.readStringUntil('\n');

    //potential inputs:
    //player stand
    //player anticlockwise
    //player clockwise
    //player horizontal
    //player kick
    //if the begining of the input is "player" execute the player segment
    if(inputline.substring(0,6) == "player"){
      Serial.println("player mode babey");
      Serial.println(inputline.substring(7));
      command = inputline.substring(7);
      command.trim();
      if (command.equals("stand")){
          stand();
        }
      else if (command.equals("kick")){
          Serial.println("kick");
          kick();
        }
      else if (command.equals("anticlockwise")){
          Serial.println("anticlockwise");
          anticlockwise();
        }
      else if (command.equals("clockwise")){
          clockwise();
        }
      else if (command.equals("horizontal")){
          horizontal();
        } 
      //previous command helps the player fuctions with some logic stuff, keep it in.
      previousCommand = command;
      }

    //potential inputs:
    //lateral reset
    //lateral in
    //lateral out
    //lateral *number between 0-110 inclusive*
    //if the begining of the input is "lateral" exeute the lateral segment
    else if (inputline.substring(0,7) == "lateral"){
      Serial.println("lateral mode");
      Serial.println(inputline.substring(8));
      movetype = inputline.substring(8);
      movetype.trim();
      //if the rest of the input is "reset" do the reset
      if(movetype == "reset"){
        resetLateral();
        }
      //if the rest of the input is "in" move all the way in
      else if(movetype == "in"){
        fullIn();
        }
      //if the rest of the input is "out" move all the way out
      else if(movetype == "out"){
        fullOut();
        }
      }
      //check if the remaining characters are all digits
      for(int i=0; i < movetype.length(); i++){
        if(!(isDigit(movetype.charAt(i)))){
          isInt = false;
        }
      }
      //if the remaing characters are digits then call the "moveTo" function with the provided number
      if(isInt){
        rotation = movetype.toInt();
        moveTo(rotation);
        }
      }
  }
  //Serial.println("counterclockwise");
  //myStepper.step(stepsPerRevolution);
  //delay(500);

  // step one revolution in the other direction:
  //Serial.println("clockwise");
  //myStepper.step(-stepsPerRevolution);
  //delay(500);
