#this file uses the three sensors to detect the scores

import serial
import time
from AppInterface import AppInterface

class GoalSensorInterface:
    #initalize player scores and sensor ports
    def __init__(self):
        #player1 human, player2 robot
        self.player_1_score = 0
        self.player_2_score = 0

        # Set the distance threshold for detecting spikes (in cm)
        self.threshold = 5

        #the game only starts when sensors from pi says so
        self.game_start = False

        # Arduino1 serial communication setup
        self.arduino_ser = serial.Serial('/dev/ttyACM2', 115200)  # Replace '/dev/ttyACM0' with the appropriate port
        self.arduino_ser.timeout = 0  # Set timeout to zero to read non-blocking
        time.sleep(1)  # Wait for the serial connection to be established

        self.time_since_last_goal = time.time()
        
        self.app_interface = AppInterface("FoozbotMobileApp-master/score.json")


        time.sleep(1)

        #all three sensors initiated
            
    def player_score(self, player_no):
        print("player score input" + str(player_no) + "\n")

        if time.time() - self.time_since_last_goal > 8:
            if player_no == 1:
                print("PLAYER 1 SCORES")
                self.player_1_score += 1
                self.app_interface.update_score((self.player_1_score, self.player_2_score))
            if player_no ==2:
                print("PLAYER 2 SCORES")
                self.player_2_score += 1
                self.app_interface.update_score((self.player_1_score, self.player_2_score))

            self.time_since_last_goal = time.time()

    def close_sensors(self):
        self.arduino_ser.close()


    def get_player_score(self, player_no):
        if player_no == 1:
            print("player 1 scores")
            return self.player_1_score
        if player_no ==2:
            print("player 2 scores")
            return self.player_2_score

    def detect_score(self):
        # the game starts once the senors from pi detects
        # Read data from TF-Luna Mini LiDAR
        
        while True:
                # Read data from Arduino sensor1
            try:
                data = self.arduino_ser.readline().strip()
            except Exception as e:
                print(e)
            
            #print(data)
            if data.startswith(b"Distance from Sensor 1: "):
                
                try:
                    values1 = data.split(b"\t")
                    distance_str1 = values1[0].split(b": ")[1].strip()
                    distance1 = float(distance_str1[:-2])  # Remove the unit "cm"
                    #print("distance 1: " + str(distance1))
                except ValueError:
                    continue  # Skip this iteration if parsing to float fails
                except IndexError:
                    continue
                print(distance1)
                if distance1 < self.threshold and distance1 > 1:
                    #print(f"Foosbot robot scores!")
                    self.player_score(1)
                    #print(f"human vs. foosbot: {self.player_1_score} vs. {self.player_2_score}")


            elif (data.startswith(b"Distance from Sensor 2:")):

                try:
                    values2 = data.split(b"\t")
                    distance_str2 = values2[0].split(b": ")[1].strip()
                    distance2 = float(distance_str2[:-2])  # Remove the unit "cm"
                except ValueError:
                    continue  # Skip this iteration if parsing to float fails
                    
                except IndexError:
                    continue
                print(distance2)    
                if distance2 < self.threshold and distance2 >1:
                    #print(f"Human player scores!")
                    self.player_score(2)
                    #print(f"human vs. foosbot: {self.player_1_score} vs. {self.player_2_score}")
                    
            else:
                continue




            time.sleep(0.01)  # Small delay to avoid excessive CPU usage


