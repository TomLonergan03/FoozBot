import unittest

from ArduinoInterface import ArduinoInterface
from Mocks.MockSerial import MockSerial


class ArduinoInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.arduino_interface = ArduinoInterface(player_1_serial=MockSerial(), player_2_serial=MockSerial())


    def test_reset_after_command(self):
        self.arduino_interface.go_vertical(1)
        self.arduino_interface.kick(1)
        self.arduino_interface.go_horizontal(2)
        self.arduino_interface.kick(2)
        self.arduino_interface.send_command()

        assert (    self.arduino_interface.kick_outp1 == 0
                and self.arduino_interface.stand_or_horiz1 == 0
                and self.arduino_interface.revolve1 == 0
                and self.arduino_interface.lat_outp1 == 777)

        assert (    self.arduino_interface.kick_outp2 == 0
                and self.arduino_interface.stand_or_horiz2 == 0
                and self.arduino_interface.revolve2 == 0
                and self.arduino_interface.lat_outp2 == 777)

