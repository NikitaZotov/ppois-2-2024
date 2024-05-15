from View.Enemys.BaseEnemy import BaseEnemy
from settings import screen_width, screen_height
class BallAlien(BaseEnemy):
    def __init__(self,x,y,enemy_data):
        super().__init__( x,y,enemy_data)
        self.speed_x= self.enemy_data.speed
        self.speed_y= self.enemy_data.speed

    def update(self, **kwargs):
        self.rect.move_ip((self.speed_x,self.speed_y))
        # Отталкивание от стенок
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > screen_height/3:
            self.speed_y = -self.speed_y