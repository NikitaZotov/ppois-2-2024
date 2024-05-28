from abc import ABC

from pygame import Vector2

from .node import Node


class GameObject(Node, ABC):
    name = "game object"

    def __init__(
            self,
            position: Vector2 = Vector2(),
            on_move=None,
    ):
        super().__init__(position)
        self.on_move = on_move

    def move(self, d: Vector2):
        self._position += d
        if self.on_move:
            self.on_move(self)

    def collision(self, node):
        pass

    def __str__(self):
        return f"{self.name} on {self.position}"
