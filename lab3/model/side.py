from enum import Enum
from pygame import Vector2


class Side(Enum):
    stop = Vector2()
    up = Vector2(0, -1)
    right = Vector2(1, 0)
    down = Vector2(0, 1)
    left = Vector2(-1, 0)

    def reverse(self):
        match self:
            case self.stop:
                return self
            case self.up:
                return self.down
            case self.right:
                return self.left
            case self.down:
                return self.up
            case self.left:
                return self.right
            case self.stop:
                return self.stop
