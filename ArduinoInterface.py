import serial


class ArduinoInterface:
    def __init__(self):
        # Arduino is always on this port
        self.serial_port = 'COM3'
        self.baud_rate = 9600

        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        # self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.kick_outp = 0      # 0 - no kick, 1 = yes kick
        self.stand_outp = 0     # 0 - remain in current pos, 1 - stand
        self.horiz_outp = 0     # 0 - remain in current pos, 1 - go horizontal feet forward, 2 - go horizontal feet backwards
        self.lat_outp = 777     # 0 - 110 - lateral movement, 777 - don't move, 999 - lateral reset

        # Experiment with these to reduce latency?
        self.ser.timeout = 0.01
        self.ser.write_timeout = 0.01

    def send_command(self, command):
        outp  = str(self.kick_outp)
        outp += str(self.stand_outp)
        outp += str(self.horiz_outp)
        outp += str(self.lat_outp)
        self.ser.write(command.encode())
        self.reset_command()
        
    def reset_command(self):
        self.kick_outp = 0
        self.stand_outp = 0
        self.horiz_outp = 0
        self.lat_outp = 777

    def go_vertical(self, player):
        if player == 2:
            self.send_command("player stand")
            self.stand_outp = 1

    def go_horizontal(self, player):
        if player == 2:
            self.send_command("player horizontal")
            self.horiz_outp = 1

    def kick(self, player):
        if player == 2:
            self.send_command(command="player kick")
            self.kick_outp = 1

    # TODO
    def move_to(self, player,  position):
        if player == 2:
            self.send_command(command=("lateral " + str(position)))
            self.lat_outp = position

    # TODO
    def get_position(self, plyer):
        return 55

    def close(self):
        self.ser.close()
