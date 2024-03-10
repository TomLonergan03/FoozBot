class MockArduinoInterface():


    def send_command(self, command):
        return None

    def go_vertical(self, player):
        return None

    def go_horizontal(self, player):
        return None

    def kick(self, player):
        return None

    # TODO
    def move_to(self, player, position):
        # need to implement
        return None

    # TODO
    def get_position(self):
        return None

    def close(self):
        return None