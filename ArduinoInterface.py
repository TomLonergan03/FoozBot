import serial
import time

# Replace '/dev/ttyACM0' with the correct port for your system.
# For Windows, it might be something like 'COM3'.
serial_port = '/dev/ttyACM0'
baud_rate = 9600  # In sync with your Arduino program

# Establishing the connection
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  # wait for the serial connection to initialize


def send_command(command):
    ser.write(command + '\n'.encode())
    time.sleep(0.1)


def go_vertical(player):
    send_command("stand")


def go_horizontal(player):
    send_command("horizontal")


def kick(player):
    send_command("kick")

def (moveTo)