import math

import pygame


class Enemy:
    def __init__(self, x, y, speed, max_health, size, sprite, dead_sprite):
        self.x = x
        self.y = y
        self.turn_angle = 0
        self.speed = speed
        self.current_health = max_health
        self.max_health = max_health
        self.cooldown = 0
        self.size = size
        self.dead_sprite = dead_sprite
        self.dead_sprite = pygame.image.load(self.dead_sprite)
        self.dead_sprite = pygame.transform.scale(self.dead_sprite, (
            34, 34)).convert_alpha()
        self.sprite = sprite
        self.sprite = pygame.image.load(self.sprite)
        self.sprite = pygame.transform.scale(self.sprite, (
            34, 34)).convert_alpha()

    def update_angle(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.turn_angle = math.atan2(dy, dx)

    def take_the_damage(self, damage):
        self.current_health -= damage

    def get_shifted_coordinates(self):
        y = self.speed * math.sin(self.turn_angle)
        x = self.speed * math.cos(self.turn_angle)
        return x, y

    def update_coordinates(self, x, y):
        self.x = x
        self.y = y


class Bat(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y, 1.1, 1, 24, "sprites/bat.png",
                       "sprites/dead_bat.png")


class Skeleton(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y, 1.1, 2, 24, "sprites/skeleton.png",
                       "sprites/dead_skeleton.png")


class Ghost(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y, 2, 2, 24, "sprites/ghost.png",
                       "sprites/dead_ghost.png")


class Werewolf(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y, 0.5, 10, 24, "sprites/werewolf.png",
                       "sprites/dead_werewolf.png")


class Zombie(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y, 1.4, 5, 24, "sprites/zombie.png",
                       "sprites/dead_zombie.png")
