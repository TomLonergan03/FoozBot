import serial


class ArduinoInterface:
    def __init__(self):
        # Arduino is always on this port
        self.serial_port = '/dev/ttyACM0'
        self.baud_rate = 9600

        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        # self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.kick_outp = 0  # 0 - no kick, 1 = yes kick
        self.stand_outp = 0  # 0 - remain in current pos, 1 - stand
        self.horiz_outp = 0  # 0 - remain in current pos, 1 - go horizontal feet forward, 2 - go horizontal feet backwards
        self.revolve = 0
        self.lat_outp = 777  # 0 - 110 - lateral movement, 777 - don't move, 999 - lateral reset

        # Experiment with these to reduce latency?
        self.ser.timeout = 1
        self.ser.write_timeout = 1

    def send_command(self):
        outp = str(self.kick_outp)
        outp += str(self.stand_outp)
        outp += str(self.horiz_outp)
        outp += str(self.revolve)
        outp += str(self.lat_outp)
        outp += '\n'
        print(outp)
        #print(isinstance(outp,str))
        self.ser.write(outp.encode('utf-8'))
        line = self.ser.readline().decode().strip()
        # Print the line
        print(line)
        # self.reset_command()

    def reset_command(self):
        self.kick_outp = 0
        self.stand_outp = 0
        self.horiz_outp = 0
        self.lat_outp = 777

    def go_vertical(self, player):
        if player == 2:
            self.stand_outp = 1
            self.send_command()

    def go_horizontal(self, player):
        if player == 2:
            self.horiz_outp = 1
            self.send_command()

    def kick(self, player):
        if player == 2:
            self.kick_outp = 1
            self.send_command()

    # TODO
    def move_to(self, player, position):
        if player == 2:
            self.lat_outp = position
            self.send_command()

    # TODO
    def get_position(self, plyer):
        return 55

    def close(self):
        self.ser.close()

    def read(self):
        try:
            while True:
                # Read a line from the serial port
                self.send_command()
                line = self.ser.readline().decode().strip()

                # Print the line
                print(line)

        except KeyboardInterrupt:
            # Close the serial port when KeyboardInterrupt (Ctrl+C) is detected
            self.ser.close()


if __name__ == '__main__':
    arduino = ArduinoInterface()
    arduino.send_command()
    arduino.kick_outp = 1
    arduino.stand_outp = 0
    arduino.horiz_outp = 0
    arduino.revolve = 0
    arduino.lat_outp = 777

    arduino.send_command()
    print("test")


    #arduino.lat_outp = 50
    #arduino.send_command()

    arduino.kick_outp = 0
    arduino.revolve = 1
    arduino.send_command()
    #arduino.send_command()

    arduino.close()


 #   arduino.read()
