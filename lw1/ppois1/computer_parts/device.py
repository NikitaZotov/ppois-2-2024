class Device:

    def __init__(self, model):
        self._model: str = model
        self.state = False

    def info(self):
        print(f"Model: {self._model}")
        print(f"State: {'On' if self.state else 'Off'}")

    def plug_in(self):
        self.state = True

    def unplug(self):
        self.state = False

    def is_peripheral(self):
        return True

    def get_model(self):
        return self._model
