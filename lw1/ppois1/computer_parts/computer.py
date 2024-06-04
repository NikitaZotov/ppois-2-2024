from computer_parts.peripheral_device import PeripheralDevice
from computer_parts.cpu import CPU
from computer_parts.ram import RAM
from computer_parts.graph_card import GraphCard
from computer_parts.hard_drive import HardDrive


class Computer:
    OS_MAX_VERSION = 2.0
    def __init__(self):
        self._version_os: float = 1.0
        self._state: bool = True
        self._cpu = CPU('base_model_cpu')
        self._hard_drive = HardDrive('base_model_hdd',10)
        self._ram = RAM('base_model_ram')
        self._graphics_card = GraphCard('base_model_gpu')
        self._peripherals = []

    @classmethod
    def check_os_version(cls, version):
        return cls.OS_MAX_VERSION > version

    def info(self):
        if self._state is not False:
            print("Спецификация компьютера:")
            print(f"Процессор: {self._cpu.get_model() if self._cpu is not None else 'Empty'}")
            print(f"Оперативная память: {self._ram.get_model()if self._ram is not None else 'Empty'}")
            print(f"Жесткий диск: {self._hard_drive.get_model()if self._hard_drive is not None else 'Empty'}")
            print(f"Видеокарта: {self._graphics_card.get_model()if self._graphics_card is not None else 'Empty'}")
            print("Периферические устройства:")
            for peripheral in self._peripherals:
                print(f"{peripheral.get_type()}: {peripheral.get_model()}")
            print(f"Версия операционной системы:{self._version_os}")
        else:
            print("Компьютер выключен")

    def get_cpu(self):
        return self._cpu

    def plug_in_cpu(self, cpu_model: str):
        if self._cpu is None:
            self._cpu = CPU(cpu_model)
            self._cpu.plug_in()
        else:
            print("В компьютере уже есть процессор")

    def plug_in_ram(self, ram_model: str):
        if self._ram is None:
            self._ram = RAM(ram_model)
            self._ram.plug_in()
        else:
            print("В компьютере уже есть оперативная память")

    def plug_in_hard_drive(self, hard_drive_model: str, capacity: int):
        if self._hard_drive is None:
            self._hard_drive = HardDrive(hard_drive_model, capacity)
            self._hard_drive.plug_in()
        else:
            print("В компьютере уже есть жесткий диск")

    def plug_in_graph_card(self, graph_card_model: str):
        if self._graphics_card is None:
            if self._state is False:
                self._graphics_card = GraphCard(graph_card_model)
                self._graphics_card.plug_in()
            else:
                print("Это не безопасно! Пожалуйста, выключите компьютер перед подключением внутренних устройств ")
        else:
            print("В компьютере уже есть видеокарта")

    def unplug_cpu(self):
        if self._state is False:
            self._cpu = None
        else:
            print("Это не безопасно! Пожалуйста, выключите компьютер перед отключением внутренних устройств")

    def unplug_ram(self):
        if self._state is False:
            self._ram = None
        else:
            print("Это не безопасно! Пожалуйста, выключите компьютер перед отключением внутренних устройств")

    def unplug_hard_drive(self):
        if self._state is False:
            self._hard_drive = None
        else:
            print("Это не безопасно! Пожалуйста, выключите компьютер перед отключением внутренних устройств")

    def unplug_graph_card(self):
        if self._state is False:
            self._graphics_card = None
        else:
            print("Это не безопасно! Пожалуйста, выключите компьютер перед отключением внутренних устройств")

    def turn_on(self):
        if self._cpu is None:
            print("В компьютере не хватает процессора.")
            return
        if self._ram is None:
            print("В компьютере не хватает оперативной памяти.")
            return
        if self._hard_drive is None:
            print("В компьютере не хватает жесткого диска.")
            return
        self._state = True

    def turn_off(self):
        self._state = False

    def connect_peripheral(self, peripheral: PeripheralDevice):
        self._peripherals.append(peripheral)
        peripheral.plug_in()

    def disconnect_peripheral(self, peripheral_model: str):
        for peripheral in self._peripherals:
            if peripheral.get_model() == peripheral_model:
                self._peripherals.remove(peripheral)
                peripheral.unplug()
                return
        print(f"Нет периферических устройств с именем: {peripheral_model}.")

    def install_software(self, address: int, software_name: str):
        if self._state is True:
            if self._hard_drive.write_data(address, software_name) is False:
                print("Не хватает памяти")
        else:
            print("Включите компьютер!")
        print(f'Теперь по адрессу {address} хранится {self._hard_drive.read_data(address)}')

    def find_data(self, address: int):
        if self._state is True:
            if self._hard_drive.read_data(address) is not None:
                print(f"По адресу {address} расположен {self._hard_drive.read_data(address)}")
                return self._hard_drive.read_data(address)
            else:
                print("По данному адресу ничего нет")
        else:
            print("Включите компьютер!")

    def del_data(self, address: int):
        if self._state is True:
            if self._hard_drive.read_data(address) is not None:
               self._hard_drive.del_data(address)
            else:
                print("По данному адресу ничего нет")
        else:
            print("Включите компьютер!")

    def update_os(self):
        if self._state is True:
            if self.check_os_version(self._version_os):
                self._version_os = self._version_os + 0.1
            else:
                print("Вы достигли максимально возможной версии")
        else:
            print("Включите компьютер")

    def get_state(self) -> bool:
        return self._state
