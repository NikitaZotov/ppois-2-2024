import pygame
from sound import Sound
from cursor import Cursor

class Bullet:
    def __init__(self):
        self.bullet = pygame.image.load("images/bullet.png").convert_alpha()
        self.bullets = 6
        self.sound = Sound()
        self.time_reload = 1001

    def print_bullet(self, num, screen):
        x_pos = 800
        for i in range(num):
            x_pos = x_pos - 40
            screen.blit(self.bullet,(x_pos,500))

    def fire(self, cursor):
        print(f"Fire: {self.time_reload}")
        if self.time_reload > 1000:
            if self.bullets > 0:
                self.bullets -= 1
                if cursor.offset > 100 and self.time_reload > 1000:
                    self.time_reload = 250
                self.sound.fire()
                return True
            else:
                self.bullets = 0
                return False
        else:
            return False

    def reload(self):
        if self.bullets < 6:
            self.bullets = 6
            self.sound.reload()
            self.time_reload = 0