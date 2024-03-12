import serial


class ArduinoInterface:
    def __init__(self):
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
        self.send_command("player stand")

    def go_horizontal(self, player):
        self.send_command("player horizontal")

    def kick(self, player):
        self.send_command("player kick")

    # TODO
    def move_to(self, player,  position):
        self.send_command("lateral " + str(position))

    # TODO
    def get_position(self, plyer):
        return None

    def close(self):
        self.ser.close()
