from settings import *


class FlagPillar(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/flag/flag_pillar.png')
        self.rect = self.image.get_frect(topleft=(x, y))
        self.old_rect = self.rect.copy()
        self.z = LAYERS['fg']


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/flag/flag.png')
        self.rect = self.image.get_frect(topleft=(x, y))
        self.z = LAYERS['bg']
        self.direction = vector(0, 1)
        self.moving_down_speed = 200
        self.game_end = False

    def update(self, delta_time):
        if self.game_end:
            self.rect.topleft += self.direction * self.moving_down_speed * delta_time
            if int(self.rect.bottom) == 352:
                self.game_end = False
        