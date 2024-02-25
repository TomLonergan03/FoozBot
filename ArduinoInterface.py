import sys
import serial
import time


class ArduinoInterface:
    # Arduino is always on this port
    serial_port = '/dev/ttyACM0'
    baud_rate = 9600

    ser = serial.Serial(serial_port, baud_rate)

    # Experiment with these to reduce latency?
    ser.timeout = 0.01
    ser.write_timeout = 0.01

    def send_command(self, command):
        self.ser.write(command.encode())

    def go_vertical(self, player):
        self.send_command("stand")

    def go_horizontal(self, player):
        self.send_command("horizontal")

    def kick(self, player):
        self.send_command("kick")

    def move_to(player, position):
        # need to implement
        return None

    def close(self):
        ser.close()
