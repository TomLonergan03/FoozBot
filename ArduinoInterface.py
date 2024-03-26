import serial


class ArduinoInterface:
    def __init__(self):
        # Arduino is always on this port
        self.player_1_port = 'COM6'
        self.player_2_port =  'COM5' # '/dev/ttyACM0'
        self.baud_rate = 9600

        # self.player1 = serial.Serial(self.player_1_port, self.baud_rate)
        self.player2 = serial.Serial(self.player_2_port, self.baud_rate)
        # self.ser = serial.Serial(self.serial_port, self.baud_rate)

        self.kick_outp1 = 0
        self.stand_outp1 = 0
        self.horiz_outp1 = 0
        self.revolve1 = 0
        self.lat_outp1 = 999

        self.kick_outp2 = 0      # 0 - no kick, 1 = yes kick
        self.stand_outp2 = 0     # 0 - remain in current pos, 1 - stand
        self.horiz_outp2 = 0     # 0 - remain in current pos, 1 - go horizontal feet forward, 2 - go horizontal feet backwards
        self.revolve2 = 0        # 0 - don't revolve, 1 - revolve clockwise, 2 - revolve anti-clockwise
        self.lat_outp2 = 999     # 0 - 110 - lateral movement, 777 - don't move, 999 - lateral reset

        # Experiment with these to reduce latency?
        # self.player1.timeout = 1
        # self.player1.write_timeout = 1
        self.player2.timeout = 1
        self.player2.write_timeout = 1

    def send_command(self):
        outp1 = str(self.kick_outp1)
        outp1 += str(self.stand_outp1)
        outp1 += str(self.horiz_outp1)
        outp1 += str(self.revolve1)
        outp1 += str(self.lat_outp1)
        outp1 += '\n'
        # print("Sending to p1: " + outp1)
        # self.player1.write(outp1.encode('utf-8'))

        outp2 = str(self.kick_outp2)
        outp2 += str(self.stand_outp2)
        outp2 += str(self.horiz_outp2)
        outp2 += str(self.revolve2)
        outp2 += str(self.lat_outp2)
        outp2 += '\n'
        print("Sending to p2: " + outp2)
        self.player2.write(outp2.encode('utf-8'))

        line = self.player2.readline().decode().strip()
        # Print the line
        print("Reading from p2: " + line)
        self.reset_command()

    def reset_command(self):
        self.kick_outp1 = 0
        self.stand_outp1 = 0
        self.horiz_outp1 = 0
        self.revolve1 = 0
        self.lat_outp1 = 777
        self.kick_outp2 = 0
        self.stand_outp2 = 0
        self.horiz_outp2 = 0
        self.revolve2 = 0
        self.lat_outp2 = 777

    def go_vertical(self, player):
        if player == 2:
            self.stand_outp2 = 1
            print("Go Vertical 2")
        elif player == 1:
            self.stand_outp1 = 1
            print("Go Vertical 1")

    def go_horizontal(self, player):
        if player == 2:
            self.horiz_outp2 = 1
        elif player == 1:
            self.horiz_outp1 = 1

    def kick(self, player):
        if player == 2:
            self.kick_outp2 = 1
        elif player == 1:
            self.kick_outp1 = 1

    # TODO
    def move_to(self, player, position):
        position = int(position)
        if player == 2:
            self.lat_outp2 = position
        elif player == 1:
            self.lat_outp1 = position

    # TODO
    def get_position(self, player):
        if player == 1:
            return 55
        elif player == 2:
            return 55

    def close(self):
        # self.player1.close()
        self.player2.close()
        pass

    def read(self):
        try:
            while True:
                # Read a line from the serial port
                self.send_command()
                line = self.player2.readline().decode().strip()

                # Print the line
                print(line)

        except KeyboardInterrupt:
            # Close the serial port when KeyboardInterrupt (Ctrl+C) is detected
            self.player2.close()

"""
if __name__ == '__main__':
    arduino = ArduinoInterface()
    arduino.send_command()
    arduino.kick_outp2 = 1
    arduino.stand_outp2 = 0
    arduino.horiz_outp2 = 0
    arduino.revolve2 = 0
    arduino.lat_outp2 = 777

    arduino.send_command()
    print("test")


    #arduino.lat_outp = 50
    #arduino.send_command()

    arduino.kick_outp2 = 0
    arduino.revolve2 = 1
    arduino.send_command()
    #arduino.send_command()

    arduino.close()


 #   arduino.read()
"""