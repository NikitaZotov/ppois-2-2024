from pygame import Vector2

from .node import Node


class Fruit(Node):
    name = "Fruit"
    
    def __init__(
            self, 
            position: Vector2 = Vector2(),
            type_=0
    ):
        super().__init__(position)
        self.type = type_
        