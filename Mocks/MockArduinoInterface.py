# class MockArduinoInterface():


#     def send_command(self, command):
#         return None

#     def go_vertical(self, player):
#         return None

#     def go_horizontal(self, player):
#         return None

#     def kick(self, player):
#         return None

#     # TODO
#     def move_to(self, player, position):
#         # need to implement
#         return None

#     # TODO
#     def get_position(self, player):
#         return 55

#     def close(self):
#         return None

class MockArduinoInterface:
    def __init__(self):
        self.kick_outp1 = 0
        self.stand_or_horiz1 = 0
        self.revolve1 = 0
        self.lat_outp1 = 999

        self.kick_outp2 = 0
        self.stand_or_horiz2 = 0
        self.revolve2 = 0
        self.lat_outp2 = 999

    def send_command(self):
        player_1_command_string, player_2_command_string = self.get_player_command_string()
        print("Sending to p1: " + player_1_command_string)
        print("Sending to p2: " + player_2_command_string)
        self.reset_command()

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
            self.stand_or_horiz1 = 2

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
    
    def get_position(self, player):
        if player == 1:
            return 55
        elif player == 2:
            return 55

    def close(self):
        pass

    def read(self):
        pass