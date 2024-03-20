import serial
import re

# Function to parse the data received from Arduino
def parse_data(data_str):
    # Regular expression to match the data format
    pattern = re.compile(r"Distance: (\d+)cm\tStrength: (\d+)\tTemp: (-?\d+)")
    match = pattern.search(data_str)
    if match:
        distance = int(match.group(1))
        strength = int(match.group(2))
        temp = int(match.group(3))
        return distance, strength, temp
    else:
        return None

# Setup serial connection (replace '/dev/ttyACM0' with the correct port)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            data = parse_data(line)
            if data:
                distance, strength, temp = data
                print(f"Distance: {distance}cm, Strength: {strength}, Temp: {temp}")
except KeyboardInterrupt:
    print("Program terminated")
finally:
    ser.close()
