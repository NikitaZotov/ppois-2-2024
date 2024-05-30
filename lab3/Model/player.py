import pygame


class Player(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed = 0

    def player_animation(self, screen_height):
        self.y += self.speed
        if self.top <= 0:
            self.top = 0
        if self.bottom >= screen_height:
            self.bottom = screen_height

    def speed(self, speed):
        self.speed = speed

    def opponent_ai(self, ball: pygame.Rect, speed):
        if self.top < ball.y:
            self.top += speed
        if self.bottom > ball.y:
            self.bottom -= speed
