#this file uses the three sensors to detect the scores

import serial
import time

class GoalSensorInterface:
    #initalize player scores and sensor ports
    def __init__(self):
        #player1 human, player2 robot
        self.player_1_score = 0
        self.player_2_score = 0

        # Set the distance threshold for detecting spikes (in cm)
        self.threshold = 6

        #the game only starts when sensors from pi says so
        self.game_start = False

        # Arduino1 serial communication setup
        self.arduino_ser1 = serial.Serial('/dev/ttyACM0', 115200)  # Replace '/dev/ttyACM0' with the appropriate port
        self.arduino_ser1.timeout = 0  # Set timeout to zero to read non-blocking
        time.sleep(1)  # Wait for the serial connection to be established

        # Arduino2 serial communication setup
        self.arduino_ser2 = serial.Serial('/dev/ttyACM1', 115200)
        self.arduino_ser2.timeout = 0  # Set timeout to zero to read non-blocking
        time.sleep(1)

        # TF-Luna Mini LiDAR serial communication setup
        self.tfluna_ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0)
        if not self.tfluna_ser.isOpen():
            self.tfluna_ser.open()
        #all three sensors initiated
            
    def player_score(self, player_no):
        if player_no == 1:
            self.player_1_score += 1
        if player_no ==2:
            self.player_2_score += 1

    def close_sensors(self):
        self.arduino_ser1.close()
        self.arduino_ser2.close()
        self.tfluna_ser.close()

    def get_player_score(self, player_no):
        if player_no == 1:
            return self.player_1_score
        if player_no ==2:
            return self.player_2_score

    def detect_score(self):
        while True:
            if self.game_start:
            # the game starts once the senors from pi detects
            # Read data from TF-Luna Mini LiDAR
                
                # Read data from Arduino sensor1
                data1 = self.arduino_ser1.readline().strip()
                if data1.startswith(b"Distance: "):
                    values1 = data1.split(b"\t")
                    distance_str1 = values1[0].split(b": ")[1].strip()
                    try:
                        distance1 = float(distance_str1[:-2])  # Remove the unit "cm"
                    except ValueError:
                        continue  # Skip this iteration if parsing to float fails
                    if distance1 <= threshold:
                        #print(f"Foosbot robot scores!")
                        self.player_score(1)
                        self.game_start = False
                        self.tfluna_ser.reset_input_buffer()
                        #print(f"human vs. foosbot: {self.player_1_score} vs. {self.player_2_score}")

            if self.game_start:
                data2 = self.arduino_ser2.readline().strip()
                if (data2.startswith(b"Distance: ")):
                    values2 = data2.split(b"\t")
                    distance_str2 = values2[0].split(b": ")[1]
                    try:
                        distance2 = float(distance_str2[:-2])  # Remove the unit "cm"
                    except ValueError:
                        continue  # Skip this iteration if parsing to float fails
                    if distance2 <= self.threshold:
                        #print(f"Human player scores!")
                        self.player_score(2)
                        self.game_start = False
                        self.tfluna_ser.reset_input_buffer()
                        #print(f"human vs. foosbot: {self.player_1_score} vs. {self.player_2_score}")


            else:
                # Read data from TF-Luna Mini LiDAR
                bytes_serial = self.tfluna_ser.read(9)  # Read 9 bytes at once
                if len(bytes_serial) == 9 and bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                    distance = (bytes_serial[2] + bytes_serial[3] * 256)
                    if distance < self.threshold:
                        self.game_start = True
                        #reset detected buffer for new game
                        self.arduino_ser1.reset_input_buffer()
                        self.arduino_ser2.reset_input_buffer()
                        #print(f"game starts!")

            time.sleep(0.01)  # Small delay to avoid excessive CPU usage

#usage from other files:
if __name__ == "__main__":
    goal_sensor_interface = GoalSensorInterface()
    try:
        goal_sensor_interface.detect_scores()
    except KeyboardInterrupt:
        goal_sensor_interface.close_connections()
