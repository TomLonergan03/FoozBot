class MockSerial:
    def __init__(self):
        pass
    def write(self, command_string):
        pass

    def readline(self):
        return bytes()