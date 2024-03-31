import serial
import time

player_1_score = 0
player_2_score = 0

# Set the distance threshold for detecting spikes (in cm)
threshold = 6

# The game only starts when sensors from Raspberry Pi signal
game_start = False
reset_buffer = False

# Arduino1 serial communication setup
arduino_ser1 = serial.Serial('/dev/ttyACM0', 115200)
arduino_ser1.timeout = 0  # Set timeout to zero to read non-blocking
time.sleep(1)

# Arduino2 serial communication setup
arduino_ser2 = serial.Serial('/dev/ttyACM1', 115200)
arduino_ser2.timeout = 0  # Set timeout to zero to read non-blocking
time.sleep(1)

# TF-Luna Mini LiDAR serial communication setup
tfluna_ser = serial.Serial("/dev/ttyS0", 115200, timeout=0)
if not tfluna_ser.isOpen():
    tfluna_ser.open()


def player_score(player_no):
    global player_1_score, player_2_score
    if player_no == 1:
        player_1_score += 1
    elif player_no == 2:
        player_2_score += 1

def close_sensors():
    arduino_ser1.close()
    arduino_ser2.close()
    tfluna_ser.close()

while True:

    if game_start:
        if not reset_buffer:
            arduino_ser1.reset_input_buffer()
            arduino_ser2.reset_input_buffer()
            reset_buffer = True
            time.sleep(1)
        # Read data from Arduino sensor1
        data1 = arduino_ser1.readline().strip()
        if data1.startswith(b"Distance: "):
            values1 = data1.split(b"\t")
            distance_str1 = values1[0].split(b": ")[1].strip()
            try:
                distance1 = float(distance_str1[:-2])  # Remove the unit "cm" from t>
            except ValueError:
                continue  # Skip this iteration if parsing to float fails
            if distance1 <= threshold:
                print(f"Foosbot robot scores!")
                player_score(1)
                game_start = False
                reset_buffer = False
                tfluna_ser.reset_input_buffer()
                print(f"human vs. foosbot: {player_1_score} vs. {player_2_score}")

        # Read data from Arduino sensor2
    if game_start:
        data2 = arduino_ser2.readline().strip()
        if (data2.startswith(b"Distance: ") and game_start):
            values2 = data2.split(b"\t")
            distance_str2 = values2[0].split(b": ")[1]
            try:
                distance2 = float(distance_str2[:-2])  # Remove the unit "cm" from t>
            except ValueError:
                continue  # Skip this iteration if parsing to float fails
            if distance2 <= threshold:
                print(f"Human player scores!")
                player_score(2)
                game_start = False
                reset_buffer = False
                tfluna_ser.reset_input_buffer()
                print(f"human vs. foosbot: {player_1_score} vs. {player_2_score}")

    else:
        # Read data from TF-Luna Mini LiDAR
        bytes_serial = tfluna_ser.read(9)  # Read 9 bytes at once
        if len(bytes_serial) == 9 and bytes_serial[0] == 0x59 and bytes_serial[1] ==>
            distance = (bytes_serial[2] + bytes_serial[3] * 256)
            if distance < threshold:
                game_start = True
                print(f"game starts!")

    time.sleep(0.01)  # Small delay to avoid excessive CPU usage

