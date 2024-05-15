from View.Enemys.BaseEnemy import BaseEnemy
from settings import screen_width, screen_height
import math
import random
import pygame
class RandomBallAlien(BaseEnemy):
    def __init__(self, x, y, enemy_data):
        super().__init__(x, y, enemy_data)
        self.angle = random.uniform(0, math.pi * 3)
        self.last_update=pygame.time.get_ticks()

    def update(self, **kwargs):
        self.rect.x += self.enemy_data.speed * math.cos(self.angle)
        self.rect.y += self.enemy_data.speed * math.sin(self.angle)


        # отталкивание от стен
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.angle = math.pi - self.angle
        if self.rect.top < 0 or self.rect.bottom > screen_height / 3:
            self.angle = -self.angle

        now = pygame.time.get_ticks()
        if now - self.last_update > 1000:
            self.last_update = now
            if random.random() < 0.05:
                self.angle += random.uniform(-0.5, 0.5)  # Adjust angle randomly
                self.enemy_data.speed *= random.uniform(0.9, 1.1)  # Adjust speed randomly

                self.angle %= math.pi * 2