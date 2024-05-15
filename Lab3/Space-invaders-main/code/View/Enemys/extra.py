from View.Enemys.BaseEnemy import BaseEnemy
from settings import screen_width
from random import choice
class Extra(BaseEnemy):
    def __init__(self,x,y, enemy_data):
        side = choice([-1, 1])
        if side == -1:
            x = screen_width + 50
        else:
            x = -50
        super().__init__(x, 80, enemy_data)
        self.speed = side*self.enemy_data.speed

    def update(self, **kwargs):
        self.rect.x += self.enemy_data.speed