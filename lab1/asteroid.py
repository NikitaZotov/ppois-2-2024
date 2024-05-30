from space_object import SpaceObject


class Asteroid(SpaceObject):
    def __init__(self, name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float):
        super().__init__(name, speed, mass, x, y, z, radius)
