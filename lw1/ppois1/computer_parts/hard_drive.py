from computer_parts.device import Device
import time


class HardDrive(Device):
    def __init__(self, model, capacity):
        super().__init__(model)
        self._capacity: int = capacity
        self._data = {}

    def write_data(self, address, data) -> bool:
        if type(address) is not int:
            raise TypeError("Адрес должен быть целым числом")
        if len(self._data) <= self.get_available_space():
            print("Загрузка...")
            time.sleep(len(data) / 5)
            self._data[address] = data
            return True
        else:
            return False

    def read_data(self, address) -> str:
        if type(address) is not int:
            raise TypeError("Адрес должен быть целым числом")
        if address in self._data:
            return self._data[address]
        else:
            return None

    def del_data(self, address):
        if type(address) is not int:
            raise TypeError("Адрес должен быть целым числом")
        del self._data[address]

    def get_available_space(self):
        used_space = sum(len(data) for data in self._data.values())
        return self._capacity - used_space
