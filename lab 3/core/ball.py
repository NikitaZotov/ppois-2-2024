import random

from core.game_screens import show_game_over_text
from game_consts import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, color=RED):
        super().__init__()
        # Создаем поверхность для мяча с прозрачностью
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2], pygame.SRCALPHA)
        # Рисуем круглую форму
        pygame.draw.circle(self.image, RED, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = 0
        self.speed_y = BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y