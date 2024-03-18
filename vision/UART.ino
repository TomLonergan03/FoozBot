typedef struct {
  int distance;
  int strength;
  int temp;
  boolean receiveComplete;
} TF;
TF Lidar = {0, 0, 0, false};

void getLidarData(TF* lidar) 
{
  static char i = 0;
  char j = 0;
  int checksum = 0;
  static int rx[9];
  if (Serial.available()) 
  {
    rx[i] = Serial.read();
    if (rx[0] != 0x59) 
    {
      i = 0;
    } 
    else if (i == 1 && rx[1] != 0x59) {
      i = 0;
    } 
    else if (i == 8) 
    {
      for (j = 0; j < 8; j++) 
      {
        checksum += rx[j];
      }
      if (rx[8] == (checksum % 256)) 
      {
          lidar->distance = rx[2] + rx[3] * 256;
          lidar->strength = rx[4] + rx[5] * 256;
          lidar->temp = (rx[6] + rx[7] * 256) / 8 - 256;
          lidar->receiveComplete = true;
      }
      i = 0;
    } 
    else 
    {
      i++;
    }
  }
}

void setup() {
  Serial.begin(115200);
}

void loop() 
{
  getLidarData(&Lidar);       //Acquisition of radar data
  if (Lidar.receiveComplete) 
  {
    Lidar.receiveComplete = false;
    Serial.print("Distance: ");
    Serial.print(Lidar.distance);
    Serial.print("cm\t");
    Serial.print("Strength: ");
    Serial.print(Lidar.strength);
    Serial.print("\t");
    Serial.print("Temp: ");
    Serial.println(Lidar.temp);
  }
}
