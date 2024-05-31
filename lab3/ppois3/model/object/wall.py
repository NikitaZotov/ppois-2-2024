from .node import Node


class Wall(Node):
    from pygame import Vector2

    name = "Wall"

    def __init__(
            self,
            sprite_type,
            rotation,
            position: Vector2 = Vector2()
    ):
        super().__init__(position)
        self.type = sprite_type
        self.rotation = rotation
