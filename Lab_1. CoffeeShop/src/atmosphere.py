class Atmosphere:
    """Atmosphere class for creating atmosphere"""

    def __init__(self) -> None:
        self.__base_atmosphere: float = 1.0
        self.__atmosphere: float = self.__base_atmosphere
        self.music: bool = False
        self.plants: int = 0
        self.decorations: int = 0

    @property
    def atmosphere(self) -> float:
        return self.__atmosphere

    def set_atmosphere(self, atmosphere: float) -> None:
        self.__base_atmosphere = atmosphere
        self.__update_atmosphere()

    def switch_music(self) -> None:
        if self.music:
            self.music = False
        else:
            self.music = True
        self.__update_atmosphere()

    def add_plants(self, plants: int = 1) -> None:
        self.plants += plants
        self.__update_atmosphere()

    def add_decorations(self, decorations: int = 1) -> None:
        self.decorations += decorations
        self.__update_atmosphere()

    def __update_atmosphere(self) -> None:
        self.__atmosphere = self.__base_atmosphere + self.plants * 3 + self.decorations * 2
        if self.music:
            self.__atmosphere = self.__atmosphere * 1.5
