from computer_parts.device import Device


class PeripheralDevice(Device):

    def __init__(self, model):
        super().__init__(model)

    def info(self):
        print("This is peripheral device")
        super().info()

    def is_peripheral(self):
        return True

    def get_type(self):
        return self.type
