import math

import pygame.sprite

from Weapon import Pistol, Uzi, AK47


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 2
        self.max_health = 300
        self.current_health = self.max_health
        self.size = 24
        self.cooldown = 0
        self.current_weapon = AK47()
        self.turn_angle = 0
        self.sprite = pygame.image.load("sprites/Pistol.png")
        self.sprite = pygame.transform.scale(self.sprite, (
            35, 35)).convert_alpha()

    def try_shoot(self):
        if self.cooldown <= 0:
            self.cooldown = self.current_weapon.cooldown
            return self.current_weapon.shoot(self.x, self.y, self.turn_angle)

    def change_weapon(self, weapon):
        self.current_weapon = weapon
        self.sprite = weapon.sprite

    def decrement_cooldown(self):
        self.cooldown -= 1

    def move_right(self):
        if self.x + self.speed < 800:
            self.x += self.speed

    def move_left(self):
        if self.x - self.speed > 0:
            self.x -= self.speed

    def move_up(self):
        if self.y - self.speed > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y + self.speed < 600:
            self.y += self.speed

    def fix_player_coords(self, width, height):
        self.x = max(0, min(self.x, width))
        self.y = max(0, min(self.y, height))

    def reduce_cooldown(self):
        self.cooldown -= 1

    def update_angle(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.turn_angle = math.atan2(dy, dx)

    # def get_corpse(self):
    #     return Corpse(self.x, self.y, "Assets\Sprites\Dead.png", self.turn_angle)
