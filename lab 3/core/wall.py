import pygame

from game_consts import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GRAY)  # Серый цвет
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - BRICK_WIDTH) // 2
        self.rect.y = (SCREEN_HEIGHT - BRICK_HEIGHT) // 2
        self.can_brake = False
    def set_break_true(self):
        self.can_brake = True