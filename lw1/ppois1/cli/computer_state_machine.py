from statemachine import State, StateMachine
from computer_parts.computer import Computer
from computer_parts.keyboard import Keyboard
from computer_parts.mouse import Mouse
from computer_parts.screen import Screen


class ComputerStateMachine(StateMachine):
    menu = State('Menu', initial=True)
    power_on = State('Power On')
    connect_internal_device = State('Connect Internal Device')
    connect_processor = State('Connect Processor')
    connect_hdd = State('Connect HDD')
    connect_ram = State('Connect RAM')
    connect_gpu = State('Connect GPU')
    connect_peripheral_device = State('Connect Peripheral Device')
    connect_keyboard = State('Connect Keyboard')
    connect_mouse = State('Connect Mouse')
    connect_screen = State('Connect Screen')
    datawork = State('Operations with data')
    download_data = State('Download Data')
    find_data = State('Find Data')
    del_data = State('Delete Data')
    disconnect_internal_device = State('Disconnect Internal Device')
    disconnect_processor = State('Disconnect Processor')
    disconnect_hdd = State('Disconnect HDD')
    disconnect_ram = State('Disconnect RAM')
    disconnect_gpu = State('Disconnect GPU')
    disconnect_peripheral_device = State('Disconnect Peripheral Device')
    update_os = State('Update OS')
    show_info = State('Show Info')
    power_off = State('Power Off')
    exit_ = State('Exit', final=True)

    move_next = (
        exit_.from_(menu, cond="is_return_backward")

        | menu.to(power_on, cond="is_power_on")
        | menu.from_(power_on, cond="is_return_backward")

        | menu.to(connect_internal_device, cond="is_connect_internal_device")
        | menu.from_(connect_internal_device, cond="is_return_backward")

        | menu.to(connect_peripheral_device, cond="is_connect_peripheral_device")
        | menu.from_(connect_peripheral_device, cond="is_return_backward")

        | menu.to(datawork, cond="is_datawork")
        | menu.from_(datawork, cond="is_return_backward")

        | datawork.to(download_data, cond="is_download_data")
        | datawork.from_(download_data, cond="is_return_backward")

        | datawork.to(find_data, cond="is_find_data")
        | datawork.from_(find_data, cond="is_return_backward")

        | datawork.to(del_data, cond="is_del_data")
        | datawork.from_(del_data, cond="is_return_backward")

        | menu.to(disconnect_internal_device, cond="is_disconnect_internal_device")
        | menu.from_(disconnect_internal_device, cond="is_return_backward")

        | menu.to(disconnect_peripheral_device, cond="is_disconnect_peripheral_device")
        | menu.from_(disconnect_peripheral_device, cond="is_return_backward")

        | menu.to(update_os, cond="is_update_os")
        | menu.from_(update_os, cond="is_return_backward")

        | menu.to(show_info, cond="is_show_info")
        | menu.from_(show_info, cond="is_return_backward")

        | menu.to(power_off, cond="is_power_off")
        | menu.from_(power_off, cond="is_return_backward")

        | connect_internal_device.to(connect_processor, cond="is_cpu")
        | connect_internal_device.from_(connect_processor, cond="is_return_backward")

        | connect_internal_device.to(connect_hdd, cond="is_hard_drive")
        | connect_internal_device.from_(connect_hdd, cond="is_return_backward")

        | connect_internal_device.to(connect_ram, cond="is_ram")
        | connect_internal_device.from_(connect_ram, cond="is_return_backward")

        | connect_internal_device.to(connect_gpu, cond="is_graphics_card")
        | connect_internal_device.from_(connect_gpu, cond="is_return_backward")

        | connect_peripheral_device.to(connect_keyboard, cond="is_keyboard")
        | connect_peripheral_device.from_(connect_keyboard, cond="is_return_backward")

        | connect_peripheral_device.to(connect_mouse, cond="is_mouse")
        | connect_peripheral_device.from_(connect_mouse, cond="is_return_backward")

        | connect_peripheral_device.to(connect_screen, cond="is_screen")
        | connect_peripheral_device.from_(connect_screen, cond="is_return_backward")

        | disconnect_internal_device.to(disconnect_processor, cond="is_cpu")
        | disconnect_internal_device.from_(disconnect_processor, cond="is_return_backward")

        | disconnect_internal_device.to(disconnect_hdd, cond="is_hard_drive")
        | disconnect_internal_device.from_(disconnect_hdd, cond="is_return_backward")

        | disconnect_internal_device.to(disconnect_ram, cond="is_ram")
        | disconnect_internal_device.from_(disconnect_ram, cond="is_return_backward")

        | disconnect_internal_device.to(disconnect_gpu, cond="is_graphics_card")
        | disconnect_internal_device.from_(disconnect_gpu, cond="is_return_backward")

        | menu.to.itself(internal=True)
        | connect_internal_device.to.itself(internal=True)
        | connect_peripheral_device.to.itself(internal=True)
        | disconnect_internal_device.to.itself(internal=True)
        | datawork.to.itself(internal=True)

    )

    def __init__(self, computer: Computer):
        self.computer = computer
        super().__init__()

    def run(self):
        while True:
            self.move_next(input())

    @staticmethod
    def is_return_backward(_input: str):
        return _input == 'r'

    @staticmethod
    def is_keyboard(_input: str):
        return _input == 'kb'

    @staticmethod
    def is_mouse(_input: str):
        return _input == 'ms'

    @staticmethod
    def is_screen(_input: str):
        return _input == 'scr'

    @staticmethod
    def is_cpu(_input: str):
        return _input == 'cpu'

    @staticmethod
    def is_hard_drive(_input: str):
        return _input == 'hd'

    @staticmethod
    def is_ram(_input: str):
        return _input == 'ram'

    @staticmethod
    def is_graphics_card(_input: str):
        return _input == 'gc'

    @staticmethod
    def is_power_on(_input: str):
        return _input == '1'

    @staticmethod
    def is_connect_internal_device(_input: str):
        return _input == '2'

    @staticmethod
    def is_connect_peripheral_device(_input: str):
        return _input == '3'

    @staticmethod
    def is_datawork(_input: str):
        return _input == '4'

    @staticmethod
    def is_download_data(_input: str):
        return _input == 'dwnl'

    @staticmethod
    def is_find_data(_input: str):
        return _input == 'find'

    @staticmethod
    def is_del_data(_input: str):
        return _input == 'del'

    @staticmethod
    def is_disconnect_internal_device(_input: str):
        return _input == '5'

    @staticmethod
    def is_disconnect_peripheral_device(_input: str):
        return _input == '6'

    @staticmethod
    def is_update_os(_input: str):
        return _input == '7'

    @staticmethod
    def is_show_info(_input: str):
        return _input == '8'

    @staticmethod
    def is_power_off(_input: str):
        return _input == '9'

    @staticmethod
    def on_enter_menu():
        print("1. Включить компьютер")
        print("2. Подключить внутреннее устройство")
        print("3. Подключить периферическое устройство")
        print("4. Работа с памятью")
        print("5. Отключить внутреннее устройство")
        print("6. Отключить периферическое устройство")
        print("7. Обновить операционную систему")
        print("8. Вывести информацию о компьютере")
        print("9. Выключить компьютер")
        print("- Завершить программу(r)")

    @staticmethod
    def on_enter_connect_internal_device():
        print("- Подключить процессор(cpu)")
        print("- Подключить жесткий диск(hd)")
        print("- Подключить оперативную память(ram)")
        print("- Подключить видеокарту(gc)")
        print("- Назад(r)")

    @staticmethod
    def on_enter_connect_peripheral_device():
        print("- Подключить клавиатуру(kb)")
        print("- Подключить мышку(ms)")
        print("- Подключить экран(scr)")
        print("- Назад(r)")

    @staticmethod
    def on_enter_disconnect_internal_device():
        print("- Отключить процессор(cpu)")
        print("- Отключить жесткий диск(hd)")
        print("- Отключить оперативную память(ram)")
        print("- Отключить видеокарту(gc)")
        print("- Назад(r)")

    @staticmethod
    def on_enter_datawork():
        print("- Скачать данные(dwnl)")
        print("- Найти данные(find)")
        print("- Удалить данные(del)")
        print("- Назад(r)")

    def on_enter_power_on(self):
        self.computer.turn_on()
        self.move_next('r')

    def on_enter_connect_processor(self):
        self.computer.plug_in_cpu(input("Введите модель процессора: "))
        self.move_next('r')

    def on_enter_disconnect_processor(self):
        self.computer.unplug_cpu()
        self.move_next('r')

    def on_enter_connect_hdd(self):
        try:
            self.computer.plug_in_hard_drive(input("Введите модель жесткого диска: "), int(input("Введите вместительность жесткого диска: ")))
        except ValueError:
            print("Вместительность должна быть целым числом")
        self.move_next('r')

    def on_enter_disconnect_hdd(self):
        self.computer.unplug_hard_drive()
        self.move_next('r')

    def on_enter_connect_ram(self):
        self.computer.plug_in_ram(input("Введите модель оперативной памяти: "))
        self.move_next('r')

    def on_enter_disconnect_ram(self):
        self.computer.unplug_ram()
        self.move_next('r')

    def on_enter_connect_gpu(self):
        self.computer.plug_in_graph_card(input("Введите модель видеокарты: "))
        self.move_next('r')

    def on_enter_disconnect_gpu(self):
        self.computer.unplug_graph_card()
        self.move_next('r')

    def on_enter_connect_keyboard(self):
        self.computer.connect_peripheral(Keyboard(input("Введите модель клавиатуры: ")))
        self.move_next('r')

    def on_enter_connect_mouse(self):
        self.computer.connect_peripheral(Keyboard(input("Введите модель мышки: ")))
        self.move_next('r')

    def on_enter_connect_screen(self):
        self.computer.connect_peripheral(Keyboard(input("Введите модель экрана: ")))
        self.move_next('r')

    def on_enter_disconnect_peripheral_device(self):
        self.computer.disconnect_peripheral(input("Введите модель периферического устройства: "))
        self.move_next('r')

    def on_enter_download_data(self):
        try:
            self.computer.install_software(int(input("Введите адрес:")), input("Введите название ПО:"))
        except ValueError:
            print("Адрес должен быть целым числом")
        self.move_next('r')

    def on_enter_find_data(self):
        try:
            self.computer.find_data(int(input("Введите адрес:")))
        except ValueError:
            print("Адрес должен быть целым числом")
        self.move_next('r')

    def on_enter_del_data(self):
        try:
            self.computer.del_data(int(input("Введите адрес:")))
        except ValueError:
            print("Адрес должен быть целым числом")
        self.move_next('r')

    def on_enter_power_off(self):
        self.computer.turn_off()
        self.move_next('r')

    def on_enter_show_info(self):
        self.computer.info()
        self.move_next('r')

    def on_enter_update_os(self):
        self.computer.update_os()
        self.move_next('r')

    def before_move_next(self):
        print()

    @staticmethod
    def on_enter_exit_():
        exit()

