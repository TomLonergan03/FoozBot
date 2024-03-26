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
        time.sleep(2)  # Wait for the serial connection to be established

        # Arduino2 serial communication setup
        self.arduino_ser2 = serial.Serial('/dev/ttyACM1', 115200)
        time.sleep(2)

        # TF-Luna Mini LiDAR serial communication setup
        self.tfluna_ser = serial.Serial("/dev/ttyS0", 115200, timeout=0)
        if self.tfluna_ser.isOpen() == False:
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
            # the game starts once the senors from pi detects
            # Read data from TF-Luna Mini LiDAR
            counter = self.tfluna_ser.in_waiting
            bytes_to_read = 9
            if counter > bytes_to_read - 1:
                bytes_serial = self.tfluna_ser.read(bytes_to_read)
                self.tfluna_ser.reset_input_buffer()
                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                    distance = (bytes_serial[2] + bytes_serial[3] * 256) / 100.0
                    if distance <= self.threshold:
                        self.game_start = True

            if (self.game_start):
                # Read data from Arduino sensor1
                if self.arduino_ser1.in_waiting > 0:
                    data1 = self.arduino_ser1.readline().strip()
                    if data1.startswith(b"Distance: "):
                        values1 = data1.split(b"\t")
                        distance_str1 = values1[0].split(b": ")[1]
                        distance1 = float(distance_str1[:-2])  # Remove the unit "cm" from the string
                        if distance1 <= self.threshold:
                            print(f"Foosbot robot scores!")
                            self.player_score(1)
                            self.game_start = False
                            print(f"human vs. foosbot: {self.player_1_score} vs. {self.player_2_score}")

                if self.arduino_ser2.in_waiting > 0:
                    data2 = self.arduino_ser2.readline().strip()
                    if data2.startswith(b"Distance: "):
                        values2 = data2.split(b"\t")
                        distance_str2 = values2[0].split(b": ")[1]
                        distance2 = float(distance_str2[:-2])  # Remove the unit "cm" from the string
                        if distance2 <= self.threshold:
                            print(f"Human player scores!")
                            self.player_score(2)
                            self.game_start = False
                            print(f"human vs. foosbot: {self.player_1_score} vs. {self.player_2_score}")

                time.sleep(0.01)  # Small delay to avoid excessive CPU usage

#usage from other files:
#if __name__ == "__main__":
    #goal_sensor_interface = GoalSensorInterface()
    #try:
        #goal_sensor_interface.detect_scores()
    #except KeyboardInterrupt:
        #goal_sensor_interface.close_connections()
