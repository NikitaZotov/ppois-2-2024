from settings import *


class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/tube.png')
        self.rect = self.image.get_frect(topleft=(x, y))
        self.old_rect = self.rect.copy()
        self.z = LAYERS['semi bg']
