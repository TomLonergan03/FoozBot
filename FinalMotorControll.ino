#include <Stepper.h>
int x = 0; //the lateral position of the motor
int step; //an index variable for lateral rotation
String inputline; //the input line for 
int strLen; //length of the input string
int curInt; //used to store the current int (ba-dum-ts) from the input line
bool runchecks; //used to know if we need to check for a reset motion
int range; //the number of steps in each rotation
int footPos = 0; // keeps track of the current foot postion of the players
//0 == down 
//1 == feet Backward
// 2 == feet forward
bool Move; //set to true if there is a relay command sent so that the motor commands aren't wastefully executed

//player motor on pins 2 & 3
#define PdirPin 2
#define PstepPin 3
//lateral motor on pins 8 & 9
#define LdirPin 8
#define LstepPin 9
//the number of steps for a full 360 on the motors
#define stepsPerRevolution 200
//relay activation on pins 6 & 7
#define powerPin1 6
#define powerPin2 7

void setup() {
  //set the pins as output
  pinMode(PstepPin, OUTPUT);
  pinMode(PdirPin, OUTPUT);
  pinMode(LstepPin, OUTPUT);
  pinMode(LdirPin, OUTPUT);
  pinMode(powerPin1, OUTPUT);
  pinMode(powerPin2, OUTPUT);

  // initialize the serial port:
  Serial.begin(9600);
}


void rotateClock(int denom, int dirPin, int stepPin){
  //function for simply rotating any motor clockwise
  //allows for fractional rotations
  digitalWrite(dirPin, HIGH);
  range = stepsPerRevolution/denom;
  for (int i = 0; i < range; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1100);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1100);
  }
}

void rotateAnti(int denom, int dirPin, int stepPin){
  //same function as above but anticlockwise
  digitalWrite(dirPin, LOW);
  range = stepsPerRevolution/denom;
  for (int i = 0; i < range; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1100);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1100);
  }
}

void kick(){
  //kicks the player
  rotateClock(4,2,3);
  delay(50);
  rotateAnti(2,2,3);
  delay(50);
  rotateClock(4,2,3);
}


//the next 2 functions turn the relays on and off
//this is so that the motors aren't constantly powered
void pon(){
  //power on
  //high turns the battery on
  digitalWrite(powerPin1,HIGH);
  digitalWrite(powerPin2,HIGH);
}

void pof(){
  //power off
  //low turns the battery off
  digitalWrite(powerPin1,LOW);
  digitalWrite(powerPin2,LOW);
}


//the next 3 functions are for changing the rotational positions
//of the players so that they dont block the ball from 
//moveing from behind
void feetBackward(){
  if (footPos == 0){
    rotateAnti(4,2,3);
    footPos = 2;
  }
  else if (footPos == 1){
    rotateClock(2,2,3);
    footPos = 2;
  }
}
void feetForward(){
  if (footPos == 0){
    rotateClock(4,2,3);
    footPos = 1;
  }
  else if (footPos == 2){
    rotateAnti(2,2,3);
    footPos = 1;
  }
}

void basePosition(){
  if (footPos == 1){
    rotateAnti(4,2,3);
    footPos = 0;
  }
  else if (footPos == 2){
    rotateClock(4,2,3);
    footPos = 0;
  }
}

//this resets the positioin of the lateral motor to a known base position
//so that the lateral position is accurate.
//called at the begining of the game
void resetLateral(){
  rotateClock(1,8,9);
  x = 110;
}


//function for moving the lateral motor. takes a single integer position
//and moves the players to that position
void moveTo(int position){
  //want the max rotation to be 110 steps
  //so "position" is between 0 and 110
  if (position > 110 || position < 0){
    return;
  }
  if(position < x){
    step = x - position;
    //in the case where the motors are mirrored simply
    //swap the LOW to HIGH and vice versa
    digitalWrite(8, LOW);
    for (int i = 0; i < step; i++){
      digitalWrite(9, HIGH);
      delayMicroseconds(650);
      digitalWrite(9, LOW);
      delayMicroseconds(650);
    }
    x = position;
  }
  else if (position > x){
    step = position - x;
    digitalWrite(8, HIGH);
    for (int i = 0; i < step; i++){
      digitalWrite(9, HIGH);
      delayMicroseconds(650);
      digitalWrite(9, LOW);
      delayMicroseconds(650);
    }
    x = position;
  }
  else if (position == x){
    return;
  }
}



// Main system loop
void loop() {
  //check for the availability of an input line
  if (Serial.available()){
    //read the input
    inputline = Serial.readStringUntil('\n');
    Move = true;

    //get the length of the input string
    //length should be between 4 and 6 inclusive
    //or exactly 3
    strLen = inputline.length();
    //if its 6 digits long it could be a reset command
    if(strLen == 6){
      runchecks = true;
    }
    //if its 3 digits long then it's a relay command
    //either power on or power off
    else if(strLen == 3){
      Move = false;
      if (inputline == "pon"){ 
        pon();
      }
      else if (inputline == "pof"){
        pof();
      }
    }
    

    //lateral moves
    if (Move){
      //parse the back end of the input string first, this causes the lateral
      //moves to be done before the player moves
      //so that the players are in line with the ball before kicking
      curInt = inputline.substring(3,strLen).toInt();
      //reset player position
      if(curInt == 999 && runchecks){
        resetLateral();  
      }
      //move player to given position
      else if(curInt < 111){
        moveTo(curInt);
      }

      //player moves have a precedence to them:
      //kick > go horizontal > 360

      //get the first player int, if 1 do a kick
      curInt = inputline.substring(0,1).toInt();
      if(curInt == 1){
        basePosition();
        kick();
      }
      //if it's 0 then check the rest of the digits
      else if (curInt == 0){
        //get the second player int
        curInt = inputline.substring(1,2).toInt();
        if (curInt == 1){
          //if 1 put the feet forward
          feetForward();
          }
        else if (curInt == 2){
          //if 2 put the feet backward
          feetBackward();
          }
        else if (curInt == 0){
          //if 0 return the feet downward and check for 360 commands
          basePosition();
          //get thrid player int
          curInt = inputline.substring(2,3).toInt();
          //if its a 1 rotate clockwise
          if (curInt == 1){
          rotateClock(1,2,3);
          }
          //if its a 2 rotate anticlockwise
          else if(curInt == 2){
            rotateAnti(1,2,3);
          }
        }
      }
    }
  }
}