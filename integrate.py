import serial
from imutils.video import VideoStream
import time
# Initialize serial connection (adjust '/dev/ttyACM0' as necessary)
ser = serial.Serial('/dev/ttyACM0', 9600)

def send_command(command):
    ser.write((command + "\n").encode())
    time.sleep(1)  # Ensure the Arduino has time to receive the command


while True:
    print("""Potential Inputs: 
    player stand
    player anticlockwise
    player clockwise
    player horizontal
    player kick
    lateral reset
    lateral in
    lateral out
    Press Q to exit!""")
    cmd = input("Please enter your command: ")
    if(cmd == 'q'):
        print("Exit")
        break
    else:    
        send_command(cmd)
