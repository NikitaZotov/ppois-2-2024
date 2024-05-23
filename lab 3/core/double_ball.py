import pygame
from game_consts import *
from ball import Ball


class DoubleBall(Ball):
    def __init__(self):
        super().__init__()
        pygame.draw.circle(self.image, PINK, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
