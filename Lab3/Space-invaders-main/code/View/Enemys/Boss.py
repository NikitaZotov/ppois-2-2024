from View.Enemys.BaseEnemy import BaseEnemy
from settings import screen_width, screen_height
from Controller.ConfigurationManager import ConfigurationManager


class Boss(BaseEnemy):
    def __init__(self, x, y, enemy_data):
        super().__init__(x, y, enemy_data)
        self.speed_x= enemy_data.speed
        self.speed_y= enemy_data.speed
        self.ConfigurationManager = ConfigurationManager()
        self.images = self.ConfigurationManager.load_images("../graphics/enemies/Boss")
        self.index = 0
        self.image=self.images[0]
        self.rect = self.images[self.index+1].get_rect(topleft = (x,y))

    def update(self, **kwargs):
        self.rect.move_ip((self.speed_x,self.speed_y))
        # Отталкивание от стенок
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > screen_height/3:
            self.speed_y = -self.speed_y

    def breaking(self):
        self.enemy_data.lives -= 1
        if self.enemy_data.lives % 3 == 0:
            self.index = (self.index + 1) % len(
                self.images)
            self.image = self.images[self.index]
