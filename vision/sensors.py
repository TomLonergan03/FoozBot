# Successful integration of three sensors.
# This code basically runs 3 sensors together: 1 connected to the Pi  and the other 2 connected to the Arduino.
# For output, we get the spikes identified by either of the sensors.
import serial
import time

# Arduino1 serial communication setup
arduino_ser1 = serial.Serial('/dev/ttyACM0', 115200)  # Replace '/dev/ttyACM0' with the appropriate port
time.sleep(2)  # Wait for the serial connection to be established

# Arduino2 serial communication setup
arduino_ser2 = serial.Serial('/dev/ttyACM1', 115200)
time.sleep(2)

# TF-Luna Mini LiDAR serial communication setup
tfluna_ser = serial.Serial("/dev/ttyS0", 115200, timeout=0)
if tfluna_ser.isOpen() == False:
    tfluna_ser.open()

# Set the distance threshold for detecting spikes (in cm)
threshold = 50

print('Starting Ranging...')
while True:
    # Read data from Arduino sensor1
    if arduino_ser1.in_waiting > 0:
        data1 = arduino_ser1.readline().strip()
        if data1.startswith(b"Distance: "):
            values1 = data1.split(b"\t")
            distance_str1 = values1[0].split(b": ")[1]
            distance1 = float(distance_str1[:-2])  # Remove the unit "cm" from the string
            if distance1 <= threshold:
                print(f"Spike detected on Arduino sensor1: {distance1} cm")
    
    # read from arduino sensor 2
    if arduino_ser2.in_waiting > 0:
        data2 = arduino_ser2.readline().strip()
        if data2.startswith(b"Distance: "):
            values2 = data2.split(b"\t")
            distance_str2 = values2[0].split(b": ")[1]
            distance2 = float(distance_str2[:-2])  # Remove the unit "cm" from >
            if distance2 <= threshold:
                print(f"Spike detected on Arduino sensor2: {distance2} cm")

    # Read data from TF-Luna Mini LiDAR
    counter = tfluna_ser.in_waiting
    bytes_to_read = 9
    if counter > bytes_to_read - 1:
        bytes_serial = tfluna_ser.read(bytes_to_read)
        tfluna_ser.reset_input_buffer()
        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
            distance = (bytes_serial[2] + bytes_serial[3] * 256) / 100.0
            if distance <= threshold:
                print(f"Spike detected on TF-Luna Mini LiDAR: {distance} cm")

    time.sleep(0.01)  # Small delay to avoid excessive CPU usage

arduino_ser1.close()
arduino_ser2.close()
tfluna_ser.close()
