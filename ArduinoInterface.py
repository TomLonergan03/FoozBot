import serial


class ArduinoInterface:
    def __init__(self, player_1_serial, player_2_serial):
        self.player1 = player_1_serial
        self.player2 = player_2_serial

        self.kick_outp1 = 0
        self.stand_or_horiz1 = 0
        self.revolve1 = 0
        self.lat_outp1 = 999

        self.kick_outp2 = 0             # 0 - no kick, 1 = yes kick
        self.stand_or_horiz2 = 0        # 0 - stand, 1 - go horizontal feet back, 2 - go horizontal feet front
        self.revolve2 = 0               # 0 - don't revolve, 1 - revolve clockwise, 2 - revolve anti-clockwise
        self.lat_outp2 = 999            # 0 - 110 - lateral movement, 777 - don't move, 999 - lateral reset

    def send_command(self):
        player_1_command_string, player_2_command_string = self.get_player_command_string()
        print("Sending to p1: " + player_1_command_string)
        self.player1.write(player_1_command_string.encode('utf-8'))

        print("Sending to p2: " + player_2_command_string)
        self.player2.write(player_2_command_string.encode('utf-8'))

        # Print the line
        line = self.player2.readline().decode().strip()
        print("Reading from p2: " + line)
        self.reset_command()

    def pon(self):
        temp = "pon"
        self.player1.write(temp.encode('utf-8'))
        self.player2.write(temp.encode('utf-8'))
    
    def poff(self):
        temp = "pof"
        self.player1.write(temp.encode('utf-8'))
        self.player2.write(temp.encode('utf-8'))

    def get_player_command_string(self):
        outp1 = str(self.kick_outp1)
        outp1 += str(self.stand_or_horiz1)
        outp1 += str(self.revolve1)
        outp1 += str(self.lat_outp1)
        outp1 += '\n'

        outp2 = str(self.kick_outp2)
        outp2 += str(self.stand_or_horiz2)
        outp2 += str(self.revolve2)
        outp2 += str(self.lat_outp2)
        outp2 += '\n'
        return outp1, outp2


    def reset_command(self):
        self.kick_outp1 = 0
        self.revolve1 = 0
        self.lat_outp1 = 777
        
        self.kick_outp2 = 0
        self.revolve2 = 0
        self.lat_outp2 = 777

    def go_vertical(self, player):
        if player == 2:
            self.stand_or_horiz2 = 0
            print("Go Vertical 2")
        elif player == 1:
            self.stand_or_horiz1 = 0
            print("Go Vertical 1")

    def go_horizontal(self, player):
        if player == 2:
            self.stand_or_horiz2 = 1
        elif player == 1:
            self.stand_or_horiz1 = 1

    def kick(self, player):
        if player == 2:
            self.kick_outp2 = 1
        elif player == 1:
            self.kick_outp1 = 1

    def move_to(self, player, position):
        position = int(position)
        if player == 2:
            self.lat_outp2 = position
        elif player == 1:
            self.lat_outp1 = position

    def fanfare(self):
        self.revolve1 = 1
        self.revolve2 = 1
    
    # TODO
    def get_position(self, player):
        if player == 1:
            return 55
        elif player == 2:
            return 55

    def close(self):
        self.player1.close()
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