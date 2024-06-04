import unittest
from computer_parts.peripheral_device import PeripheralDevice
from computer_parts.cpu import CPU
from computer_parts.ram import RAM
from computer_parts.graph_card import GraphCard
from computer_parts.hard_drive import HardDrive
from computer_parts.computer import Computer


class TestComputer(unittest.TestCase):

    def setUp(self):
        self.computer = Computer()

    def test_initial_state(self):
        self.assertEqual(self.computer.get_state(), True)
        self.assertEqual(self.computer._version_os, 1.0)
        self.assertIsInstance(self.computer.get_cpu(), CPU)

    def test_turn_on_without_cpu(self):
        self.computer.turn_off()
        self.computer.unplug_cpu()
        self.computer.turn_on()
        self.assertEqual(self.computer.get_state(), False)

    def test_turn_on_with_cpu(self):
        self.computer.turn_off()
        self.computer.turn_on()
        self.assertEqual(self.computer.get_state(), True)

    def test_plug_in_cpu(self):
        self.computer.unplug_cpu()
        self.computer.turn_off()
        self.computer.plug_in_cpu('test_cpu_model')
        self.assertIsInstance(self.computer.get_cpu(), CPU)

    def test_plug_in_ram(self):
        self.computer.unplug_ram()
        self.computer.turn_off()
        self.computer.plug_in_ram('test_ram_model')
        self.assertIsInstance(self.computer._ram, RAM)

    def test_plug_in_hard_drive(self):
        self.computer.unplug_hard_drive()
        self.computer.turn_off()
        self.computer.plug_in_hard_drive('test_hdd_model', 500)
        self.assertIsInstance(self.computer._hard_drive, HardDrive)

    def test_plug_in_graph_card(self):
        self.computer.unplug_graph_card()
        self.computer.turn_off()
        self.computer.plug_in_graph_card('test_gpu_model')
        self.assertIsInstance(self.computer._graphics_card, GraphCard)

    def test_update_os(self):
        self.computer.update_os()
        self.assertEqual(self.computer._version_os, 1.1)

    def test_install_data(self):
        self.computer.turn_on()
        self.computer.install_software(1, 'Test Software')
        self.assertEqual(self.computer.find_data(1), 'Test Software')

    def test_del_data(self):
        self.computer.turn_on()
        self.computer.install_software(0, 'Test Software')
        self.computer.del_data(0)
        data = self.computer.find_data(0)
        self.assertIsNone(data)

    def test_connect_peripheral(self):
        peripheral = PeripheralDevice('test_peripheral')
        self.computer.connect_peripheral(peripheral)
        self.assertIn(peripheral, self.computer._peripherals)

    def test_disconnect_peripheral(self):
        peripheral = PeripheralDevice('test_peripheral')
        self.computer.connect_peripheral(peripheral)
        self.computer.disconnect_peripheral('test_peripheral')
        self.assertNotIn(peripheral, self.computer._peripherals)

    def test_check_os_version(self):
        self.computer.turn_on()
        self.assertTrue(Computer.check_os_version(1.5))
        self.assertFalse(Computer.check_os_version(2.0))

if __name__ == "__main__":
    unittest.main()
