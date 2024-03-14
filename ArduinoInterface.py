import serial


class ArduinoInterface:
    def __init__(self):
        # Arduino is always on this port
        self.serial_port = 'COM3'
        self.baud_rate = 9600

        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        # self.ser = serial.Serial(self.serial_port, self.baud_rate)

        # Experiment with these to reduce latency?
        self.ser.timeout = 0.01
        self.ser.write_timeout = 0.01

    def send_command(self, command):
        self.ser.write(command.encode())

    def go_vertical(self, player):
        if player == 2:
            self.send_command("player stand")

    def go_horizontal(self, player):
        if player == 2:
            self.send_command("player horizontal")

    def kick(self, player):
        if player == 2:
            self.send_command(command="player kick")

    # TODO
    def move_to(self, player,  position):
        if player == 2:
            self.send_command(command=("lateral " + str(position)))

    # TODO
    def get_position(self, plyer):
        return 55

    def close(self):
        self.ser.close()
