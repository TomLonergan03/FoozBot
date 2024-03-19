#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
int x = 0; //x is the lateral position of the motor
int step;
String mode;
String inputline;
int strLen;
int curInt;
bool kicked = false;
bool stood = false;
bool horizontaled;
bool runchecks;
bool feetforward;

//player motor on pins 2 & 3
#define PdirPin 2
#define PstepPin 3

//lateral motor on pins 8 & 9
#define LdirPin 8
#define LstepPin 9
#define stepsPerRevolution 200

void setup() {
  //set the pins as output
  pinMode(PstepPin, OUTPUT);
  pinMode(PdirPin, OUTPUT);
  pinMode(LstepPin, OUTPUT);
  pinMode(LdirPin, OUTPUT);

  // initialize the serial port:
  Serial.begin(9600);
}

void rotateClock(int denom, int dirPin, int stepPin){
  digitalWrite(dirPin, HIGH);
  for (int i = 0; i < stepsPerRevolution/denom; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(700);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(700);
  }
}

void rotateAnti(int denom, int dirPin, int stepPin){
  digitalWrite(dirPin, LOW);
  for (int i = 0; i < stepsPerRevolution/denom; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(700);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(700);
  }
}

void kick(){
  rotateAnti(4,2,3);
  delayMicroseconds(10000);
  rotateClock(2,2,3);
  delayMicroseconds(10000);
  rotateAnti(4,2,3);
}

void feetForward(){
  rotateClock(4,2,3);
}
void feetBackward(){
  rotateAnti(4,2,3);
}
void stand(){
  basePosition();
}

void basePosition(){
  if(horizontaled && feetforward){
    rotateAnti(4,2,3);
  }
  else if(horizontaled){
    rotateClock(4,2,3);
  }
}

void resetLateral(){
  rotateAnti(1,8,9);
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
    step = position - x;
    //rotate anticlockwise to get to the spot
    digitalWrite(8, LOW);
    for (int i = 0; i < step; i++){
      digitalWrite(9, HIGH);
      delayMicroseconds(600);
      digitalWrite(9, LOW);
      delayMicroseconds(600);
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
      delayMicroseconds(550);
      digitalWrite(9, LOW);
      delayMicroseconds(550);
    }
    x = position;
  }
  else if (position == x){
    Serial.println("same position, no move");
    return;
  }
}



// Main system loop
void loop() {
  //Im not adding anymore documentation because it works and I want this to be exactly 200 lines
  if (Serial.available()){
    //read the input
    inputline = Serial.readStringUntil('\n');
    Serial.println(inputline);

    //get the length of the input string
    //length should be between 5 and 7 inclusive
    strLen = inputline.length();
    if(strLen == 7){
      runchecks = true;
    }

    //reset the player position if needed
    basePosition();

    //get the first player int, if 1 do a kick
    curInt = inputline.substring(0,1).toInt();
    if(curInt == 1){
      kick();
      kicked = true;
    }
    else{
      kicked = false;
    }
    if (kicked == false){
      //if the played hasn't kicked
      curInt = inputline.substring(1,2).toInt();
      if (curInt == 1){
        stand();
        stood = true;
      }
      else{
        stood = false;
      }
      if(stood == false){
        curInt = inputline.substring(2,3).toInt();
        if (curInt == 1){
          feetForward();
          feetforward = true;
          horizontaled = true;
        }
        else if (curInt == 2){
          feetBackward();
          feetforward = false;
          horizontaled = true;
        }
        else{
          horizontaled = false;
        }
        if(horizontaled == false){
          curInt = inputline.substring(3,4).toInt();
          if (curInt == 1){
            rotateClock(1,2,3);
          }
          else if(curInt == 2){
            rotateAnti(1,2,3);
          }
        }
      }
    }
    //onto the lateral moves
    curInt = inputline.substring(4,strLen).toInt();
    if(curInt == 999 && runchecks){
      resetLateral();  
    }
    else if(curInt < 111){
      moveTo(curInt);
    }
  }
}