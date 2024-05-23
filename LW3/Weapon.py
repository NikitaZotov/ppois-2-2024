import random

import pygame

from Shoot import Shoot


class Weapon:
    def __init__(self, damage, speed, accuracy, cooldown, sprite, laying_sprite, sound):
        self.damage = damage
        self.speed = speed
        self.accuracy = accuracy
        self.cooldown = cooldown
        self.sound = sound
        self.laying_sprite = laying_sprite
        self.sprite = sprite
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, (
            34, 34)).convert_alpha()
        self.laying_sprite = laying_sprite
        self.laying_sprite = pygame.image.load(self.laying_sprite)
        self.laying_sprite = pygame.transform.scale(self.laying_sprite, (
            20, 20)).convert_alpha()

    def modify_angle(self, accuracy, turn_angle):
        return turn_angle * random.uniform(accuracy, 2 - accuracy)

    def shoot(self, x, y, turn_angle):
        return Shoot(self, x, y, self.modify_angle(self.accuracy, turn_angle), self.damage, 5, 10, self.speed,
                     "sprites/shot.png")


class Pistol(Weapon):
    def __init__(self):
        super().__init__(damage=2, speed=20, accuracy=0.98, cooldown=20,
                         sprite="sprites/Pistol.png",
                         laying_sprite="sprites/pistol_laying.png",
                         sound="sounds/pistol_sound.mp3")


class Uzi(Weapon):
    def __init__(self):
        super().__init__(damage=2, speed=20, accuracy=0.7, cooldown=7,
                         sprite="sprites/UZI.png",
                         laying_sprite="sprites/uzi_laying.png",
                         sound="sounds/uzi_sound.mp3")


class AK47(Weapon):
    def __init__(self):
        super().__init__(damage=4, speed=18, accuracy=0.8, cooldown=15,
                         sprite="sprites/AK47.png",
                         laying_sprite="sprites/ak47_laying.png",
                         sound="sounds/ak47_sound.mp3")


class Deagle(Weapon):
    def __init__(self):
        super().__init__(damage=20, speed=20, accuracy=0.98, cooldown=25,
                         sprite="sprites/Deagle.png",
                         laying_sprite="sprites/deagle_laying.png",
                         sound="sounds/deagle_sound.mp3")
