import random

import pygame
from pygame.sprite import Sprite

from core.game_consts import SCREEN_WIDTH


# Define a new class for the meteorite sprite
class Meteor(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("../static/img/meteor.png").convert_alpha(), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, abs(SCREEN_WIDTH - self.rect.width))
        self.rect.y = -self.rect.height
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y