import pygame
from game_consts import *


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
