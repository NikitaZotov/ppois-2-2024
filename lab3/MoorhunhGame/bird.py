import pygame
import random
import json
import os

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load("images/chicken1.png"),
                       pygame.image.load("images/chicken2.png"),
                       pygame.image.load("images/chicken3.png"),
                       pygame.image.load("images/chicken4.png"),
                       pygame.image.load("images/chicken5.png"),
                       pygame.image.load("images/chicken6.png"),
                       pygame.image.load("images/chicken7.png"),
                       pygame.image.load("images/chicken8.png")]
        self.index = 0
        self.shift = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(list(range(-100, -49)) + list(range(1500, 1541))), random.randint(30,570))
        self.speed = random.uniform(1, 1)
        self.direction = random.choice([-1, 1])
        self.animation_timer = pygame.time.get_ticks()
        self.animation_delay = 100
        self.zoom = 0
        self.scale_x = 100
        self.scale_y = 50
        self.pars_parametrs()
        self.scale_images(1)

    def pars_parametrs(self):
        file_list = os.listdir("config/")
        random_file = random.choice(file_list)
        print(random_file)
        merged_filepath = os.path.join("config", random_file)
        with open(merged_filepath) as file:
            data = json.load(file)
        self.speed = data["speed"]
        self.direction = data["direction"]
        x = data["position_x"]
        y = data["position_y"]
        self.rect.center = (x,y)
        self.scale_x = data["scale_x"]
        self.scale_y = data["scale_y"]
        self.score = data["score"]

    def scale_images(self, scale):
        images = []
        for image in self.images:
            images.append(pygame.transform.scale(image,(self.scale_x*scale,self.scale_y*scale)))
        self.images = images

    def update(self,additional_speed, number):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_delay:
            self.animation_timer = pygame.time.get_ticks()
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            if self.direction < 0:
                self.image = pygame.transform.flip(self.image,True,False)

        if self.shift == 2:
            self.shift = 0
            if additional_speed > 0:
                additional_speed = -1
            elif additional_speed < 0:
                additional_speed = 1
        else:
            self.shift += 1
            additional_speed = 0

        zoom = self.check_zoom(number)
        if zoom != 0:
            if self.direction * self.speed + additional_speed + zoom == 3 or self.direction * self.speed + additional_speed + zoom == -3:
                print(f"With zoom: {self.direction * self.speed + additional_speed + zoom}")
        self.rect.move_ip(self.direction * self.speed + additional_speed + zoom, 0)
        if self.rect.left > 1540 or self.rect.right < -100:
            self.kill()

    def check_zoom(self,number):
        if number == 2:
            self.zoom += 1
        else:
            self.zoom = 0

        if self.zoom == 4:
            self.zoom = 0
            if self.direction < 0:
                return -1
            else:
                return 1
        else:
            return 0