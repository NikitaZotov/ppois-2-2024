from planet import Planet


class Satellite(Planet):
    def __init__(self,  name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float, planet: Planet) -> None:
        super().__init__(name, speed, mass, x, y, z, radius)
        self.planet = planet

    def get_planet(self) -> Planet:
        return self.planet

