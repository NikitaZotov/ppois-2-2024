from space_object import SpaceObject


class Star(SpaceObject):
    def __init__(self, name: str, type_star: str, speed: float, mass: float, x: float, y: float, z: float, radius: float) -> None:
        super().__init__(name, speed, mass, x, y, z, radius)
        self.__type = type_star

    def get_type(self) -> str:
        return self.__type
