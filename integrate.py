import serial
import time
import BallDetection as bd

# Initialize serial connection (adjust '/dev/ttyACM0' as necessary)
ser = serial.Serial('/dev/ttyACM0', 9600)

def send_command(command):
    ser.write((command + "\n").encode())
    time.sleep(1)  # Ensure the Arduino has time to receive the command

while True:
    ball_position = bd.get_ball_center()
    # Logic to determine ball position
    if ball_position: # Let's have the ball's centre coords here
        send_command("kick")

