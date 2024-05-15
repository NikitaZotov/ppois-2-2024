import pygame

from Controller.ConfigurationManager import ConfigurationManager
class Explosion(pygame.sprite.Sprite):
    def __init__(self,screen, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.screen=screen
        self.frame_index = 0
        self.animation_speed = 0.1  # Скорость анимации (чем меньше, тем быстрее)
        self.ConfigurationManager = ConfigurationManager()
        self.images = self.ConfigurationManager.load_images("../graphics/explosion")

    def update(self):
        self.frame_index += self.animation_speed
        if int(self.frame_index) >= len(self.images):
            del self
        else:
            self.screen.blit(self.images[int(self.frame_index)], (self.x, self.y))

    def play_sound(self):
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.7)
        self.explosion_sound.play()


