from pygame import Vector2


class Node:
    name = 'Node'

    def __init__(
            self,
            position: Vector2 = Vector2(0, 0),
    ):
        self._position = position

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    def kill(self):
        pass

    def __copy__(self):
        return Node(self.position)

    def __str__(self):
        return f"{self.name} on {self.position}"
