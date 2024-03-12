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

//player motor on pins 2 & 3
#define PdirPin 2
#define PstepPin 3
//lateral motor on pins 8 & 9
#define LdirPin 8
#define LstepPin 9
#define stepsPerRevolution 200

// initialize the stepper libraries for both motors.
Stepper lateralStepper(stepsPerRevolution, 8, 9, 10, 11);
Stepper playerStepper(stepsPerRevolution,2,3,4,5);

void setup() {
  //set the pins as output
  pinMode(PstepPin, OUTPUT);
  pinMode(PdirPin, OUTPUT);
  pinMode(LstepPin, OUTPUT);
  pinMode(LdirPin, OUTPUT);
  // set the speed at 60 rpm:
  lateralStepper.setSpeed(40);
  playerStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);
}

void rotateClock(int denom, int dirPin, int stepPin){
  digitalWrite(dirPin, HIGH);
  for (int i = 0; i < stepsPerRevolution/denom; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(750);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(750);
  }
}

void rotateAnti(int denom, int dirPin, int stepPin){
  digitalWrite(dirPin, LOW);
  for (int i = 0; i < stepsPerRevolution/denom; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(750);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(750);
  }
}

void kick(){
  rotateClock(4,2,3);
  delayMicroseconds(10000);
  rotateAnti(2,2,3);
  delayMicroseconds(10000);
  rotateClock(4,2,3);


  //playerStepper.step(stepsPerRevolution/4);
  //playerStepper.step(-stepsPerRevolution/2);
  //playerStepper.step(stepsPerRevolution/4);
}

void horizontal(){
  rotateClock(4,2,3);
  //playerStepper.step(stepsPerRevolution/4);
}

//void clockwise(){
//  playerStepper.step(-stepsPerRevolution);
//}

//void anticlockwise(){
//  playerStepper.step(stepsPerRevolution);
//}

void stand(){
  if (previousCommand.equals("horizontal")){
      rotateAnti(4,2,3);
      //playerStepper.step(-stepsPerRevolution/4);
    }
}

void basePosition(){
  if(previousCommand.equals("horizontal") && !command.equals("stand")){
    rotateAnti(4,2,3);
    //playerStepper.step(-stepsPerRevolution/4);
  }
}

void resetLateral(){
  //lateralStepper.step(-1.5*stepsPerRevolution);
  rotateAnti(1,8,9);
  x = 110;
}

void sendPosition(){
  Serial.println(x);
}

void moveTo(int position){
  //11/22
  //want the max rotation to be 110 steps
  //so "position" is between 0 and 110
  if (position > 110 || position < 0){
    return;
  }
  if(position > x){
    step = position - x;
    //rotate anticlockwise to get to the spot
    digitalWrite(8, LOW);
    for (int i = 0; i < step; i++){
      digitalWrite(9, HIGH);
      delayMicroseconds(500);
      digitalWrite(9, LOW);
      delayMicroseconds(500);
    }
    //lateralStepper.step(-step);
    x = position;
  }
  else if (position < x){
    //clockwise to get to the spot
    step = x - position;
    digitalWrite(8, HIGH);
    for (int i = 0; i < step; i++){
      digitalWrite(9, HIGH);
      delayMicroseconds(500);
      digitalWrite(9, LOW);
      delayMicroseconds(500);
    }
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
    //read the input
    inputline = Serial.readStringUntil('\n');

    //reset the player position
    basePosition();
    //potential inputs:
    //player stand
    //player anticlockwise
    //player clockwise
    //player horizontal
    //player kick
    //if the begining of the input is "player" execute the player segment
    if(inputline.substring(0,6) == "player"){
      //playerStepper.step(stepsPerRevolution);
      //Serial.println("player mode babey");
      //Serial.println(inputline.substring(7));
      command = inputline.substring(7);
      command.trim();
      if (command.equals("stand")){
          Serial.println("stand");
          stand();
        }
      else if (command.equals("kick")){
          Serial.println("kick");
          //Serial.println("kick");
          kick();
        }
      else if (command.equals("anticlockwise")){
          Serial.println("anticlockwise");
          rotateAnti(1,2,3);
          //anticlockwise();
        }
      else if (command.equals("clockwise")){
          Serial.println("clockwise");
          rotateClock(1,2,3);
          //clockwise();
        }
      else if (command.equals("horizontal")){
          Serial.println("horizontal");
          horizontal();
        } 
      //previous command helps the player fuctions with some logic stuff, keep it in.
      previousCommand = command;
    }

    //potential inputs:
    //lateral reset
    //lateral in
    //lateral out
    //lateral position
    //lateral *number between 0-110 inclusive*
    //if the begining of the input is "lateral" exeute the lateral segment
    else if (inputline.substring(0,7) == "lateral"){
      //lateralStepper.step(stepsPerRevolution);
      isInt = true;
      Serial.println("lateral mode");
      //Serial.println(inputline.substring(8));
      movetype = inputline.substring(8);
      movetype.trim();

      for(int i=0; i < movetype.length(); i++){
        //Serial.println((isDigit(movetype.charAt(i))));
        if(!(isDigit(movetype.charAt(i)))){
          //Serial.println("not int");
          isInt = false;
        }
      }
      if(isInt){
        Serial.println("move");
        rotation = movetype.toInt();
        moveTo(rotation);
        }
      //if the rest of the input is "reset" do the reset
      else if(movetype == "reset"){
        Serial.println("reset");
        resetLateral();
        }
      //if the rest of the input is "in" move all the way in
      else if(movetype == "in"){
        Serial.println("in");
        fullIn();
        }
      //if the rest of the input is "out" move all the way out
      else if(movetype == "out"){
        fullOut();
        }
      
      else if(movetype == "position"){
        Serial.println("send pos");
        sendPosition();
      }
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
