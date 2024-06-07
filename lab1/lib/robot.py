from colorama import Fore

from lib.cell import Cell
from lib.cell_generator import CellGenerator
from lib.robot_parts.battery import Battery
from lib.robot_parts.software import Software
from lib.robot_parts.mechanism import Mechanism
from lib.sensors.humidity_sensor import HumiditySensor
from lib.sensors.temperature_sensor import TemperatureSensor
from lib.sensors.electrification_sensor import ElectrificationSensor


class Robot(object):
    def __init__(self):
        self.battery = Battery()
        self.software = Software()
        self.sensors = [ElectrificationSensor(), TemperatureSensor(), HumiditySensor()]
        self.mechanism = Mechanism()

    @property
    def details(self) -> list:
        return [self.battery, self.software]

    def auto_move(self, moves_number: int, auto_help = True) -> None:
        if moves_number < 0:
            raise ValueError("Robot can't do negative number of moves")

        for i in range(moves_number):
            print(f"{Fore.LIGHTWHITE_EX}")
            if i > 0:
                print("="*128)
            print("Trying to move")
            cells = CellGenerator.generate_cells()
            Robot.show_cells(cells)
            try:
                print("Getting charge from battery")
                self.battery.get_low()
                print("Software's choosing cell")
                cell = self.software.choose_cell(self.sensors, cells)
                print("Chosen Cell: ", cell)
                self.mechanism.move(cell)
            except ValueError as e:
                print(f"{Fore.YELLOW}{e}")
                if auto_help:
                    from lib.support_team import SupportTeam
                    SupportTeam.fix_problem(self)
                    i -= 1
                    continue
                while True:
                    command = input('Robot needs help, call support team by "help"'
                                    '(or "leave" to leave robot with his problems alone): ')
                    if command == "help":
                        from lib.support_team import SupportTeam
                        SupportTeam.fix_problem(self)
                        i -= 1
                        break
                    if command == "leave":
                        return
                    print("Strange command, try again")

    @staticmethod
    def show_cells(cells: list[Cell]) -> None:
        print("Current cells: ")
        for cell in cells:
            print("- ", cell)
