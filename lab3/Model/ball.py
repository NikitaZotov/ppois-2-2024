import pygame


class Ball(pygame.Rect):
    def __init__(self, x, y, width=30, height=30, speed=7):
        self.speed_x = speed
        self.speed_y = speed
        self.sound = pygame.mixer.Sound("D:/lab1/ppois3/Model/sounds/pong.ogg")
        super().__init__(x, y, width, height)

    def ball_animation(self, screen_height):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.top <= 0 or self.bottom >= screen_height:
            self.speed_y *= -1
            pygame.mixer.Sound.play(self.sound)


