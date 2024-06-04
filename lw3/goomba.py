import pygame

from settings import *
from sprites import Sprite


class Goomba(Sprite):
    def __init__(self, pos, frames, level, z, speed, animation_speed=ANIMATION_SPEED):
        # animation
        self.frames, self.frame_index = frames, 0
        self.state = 'movement'
        self.animation_speed = animation_speed

        # general
        super().__init__(pos, frames[self.state][self.frame_index], [level.all_sprites, level.collision_sprites], z)
        self.level = level
        self.dead = False

        # movement
        self.ability_to_move = True
        self.speed = speed
        self.direction = vector()
        self.gravity = 500
        self.on_floor = False
        self.move_left = False

    def killed(self):
        self.state = 'dead'
        self.ability_to_move = False
        self.dead = True

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.level.collision_sprites]
        self.on_floor = True if floor_rect.collidelist(collide_rects) >= 0 else False

        left_rect = pygame.Rect((self.rect.topleft[0] - 2, self.rect.topleft[1]), (2, self.rect.height))
        self.move_left = False if left_rect.collidelist(collide_rects) >= 0 else True

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

    def update(self, delta_time):
        self.animate(delta_time)
        if self.ability_to_move:
            self.check_contact()
            self.direction.x = -1 if self.move_left else 0
            self.direction.y = 1 if not self.on_floor else 0
            self.old_rect = self.rect.copy()
            self.rect.topleft += self.direction * self.speed * delta_time
