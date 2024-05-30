import random
from spacecraft import Spacecraft
from star import *
from space_object import SpaceObject


class Planet(SpaceObject):
    def __init__(self,  name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float,
                 star: Star = None) -> None:
        super().__init__(name, speed, mass, x, y, z, radius, atmosphere=self.generate_atmosphere())
        self.__star = star

    def generate_atmosphere(self):
        count = 5
        random_floats = []

        # Генерируем случайные числа и добавляем их в список
        for _ in range(count - 1):
            last_atmosphere = 100-sum(random_floats)
            random_float = random.uniform(0, last_atmosphere)
            random_floats.append(random_float)

        # Последний элемент списка выбирается таким образом, чтобы сумма всех чисел была равна 100
        last_float = 100 - sum(random_floats)
        random_floats.append(last_float)

        return random_floats

    def start_spacecraft(self, name: str) -> Spacecraft:
        return Spacecraft(name, self)


if __name__ == "__main__":
    a = Planet('earth', 4.2, 2, 20, 2, 3, 4)

    print(a.get_atmosphere())
    data = a.get_atmosphere()
    res = 0
    for i in data:
        res += i
    print(res)
