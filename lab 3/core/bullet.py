import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, paddle):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("../static/img/bullet.png").convert_alpha(), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
