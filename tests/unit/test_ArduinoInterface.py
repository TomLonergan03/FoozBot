import unittest
from unittest.mock import MagicMock
from ArduinoInterface import ArduinoInterface

class ArduinoInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.player_1_serial = MagicMock()
        self.player_2_serial = MagicMock()
        self.arduino_interface = ArduinoInterface(player_1_serial=self.player_1_serial, player_2_serial=self.player_2_serial)

    def test_reset_after_command(self):
        self.arduino_interface.go_vertical(1)
        self.arduino_interface.kick(1)
        self.arduino_interface.go_horizontal(2)
        self.arduino_interface.kick(2)
        self.arduino_interface.send_command()
        self.assert_reset_state()

    def test_go_vertical(self):
        self.arduino_interface.go_vertical(1)
        self.assertEqual(self.arduino_interface.stand_outp1, 1)
        self.arduino_interface.go_vertical(2)
        self.assertEqual(self.arduino_interface.stand_outp2, 1)

    def test_go_horizontal(self):
        self.arduino_interface.go_horizontal(1)
        self.assertEqual(self.arduino_interface.horiz_outp1, 1)
        self.arduino_interface.go_horizontal(2)
        self.assertEqual(self.arduino_interface.horiz_outp2, 1)

    def test_kick(self):
        self.arduino_interface.kick(1)
        self.assertEqual(self.arduino_interface.kick_outp1, 1)
        self.arduino_interface.kick(2)
        self.assertEqual(self.arduino_interface.kick_outp2, 1)

    def test_move_to(self):
        self.arduino_interface.move_to(1, 50)
        self.assertEqual(self.arduino_interface.lat_outp1, 50)
        self.arduino_interface.move_to(2, 80)
        self.assertEqual(self.arduino_interface.lat_outp2, 80)

    def test_get_position(self):
        position1 = self.arduino_interface.get_position(1)
        self.assertEqual(position1, 55)
        position2 = self.arduino_interface.get_position(2)
        self.assertEqual(position2, 55)

    def test_send_command(self):
        self.arduino_interface.send_command()
        self.player_1_serial.write.assert_called_once_with(b"0000999\n")
        self.player_2_serial.write.assert_called_once_with(b"0000999\n")
        self.assert_reset_state()

    def assert_reset_state(self):
        self.assertEqual(self.arduino_interface.kick_outp1, 0)
        self.assertEqual(self.arduino_interface.stand_outp1, 0)
        self.assertEqual(self.arduino_interface.horiz_outp1, 0)
        self.assertEqual(self.arduino_interface.revolve1, 0)
        self.assertEqual(self.arduino_interface.lat_outp1, 777)
        self.assertEqual(self.arduino_interface.kick_outp2, 0)
        self.assertEqual(self.arduino_interface.stand_outp2, 0)
        self.assertEqual(self.arduino_interface.horiz_outp2, 0)
        self.assertEqual(self.arduino_interface.revolve2, 0)
        self.assertEqual(self.arduino_interface.lat_outp2, 777)

if __name__ == '__main__':
    unittest.main()