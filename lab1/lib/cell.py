class Cell(object):
    def __init__(self, electrification: int, temperature: int, humidity: int):
        if electrification < 0 or temperature < 0 or humidity < 0:
            raise ValueError("Cells can't exist with negative values")

        self._electrification = electrification if electrification <= 100 else 100
        self._temperature = temperature if temperature <= 100 else 100
        self._humidity = humidity if humidity <= 100 else 100

    @property
    def humidity(self) -> int:
        return self._humidity

    @property
    def temperature(self) -> int:
        return self._temperature

    @property
    def electrification(self) -> int:
        return self._electrification

    def __str__(self):
        return f"Cell with electrification: {self.electrification}, " \
               f"humidity: {self.humidity}, temperature: {self.temperature}"
