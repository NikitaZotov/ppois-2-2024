import pygame
from Weapon.PlayerLaser import PlayerLaser
from Weapon.PlayerBigLaser import PlayerBigLaser
from Controller.ConfigurationManager import ConfigurationManager
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed, lives):
        super().__init__()
        self.speed = speed
        self.max_x_constraint = constraint  # ограничение перемещения по x
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600  # время остывания лазера

        self.lasers = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)

        self.ConfigurationManager = ConfigurationManager()
        self.images = self.ConfigurationManager.load_images("../graphics/player")
        self.lives=lives
        self.index = 3
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.weapon_type="laser"
        self.last_update = pygame.time.get_ticks()


    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        if self.weapon_type=="BigLaser":
            self.lasers.add(PlayerBigLaser(self.rect.center,-8, self.rect.bottom, 5000))
        else:
            self.lasers.add(PlayerLaser(self.rect.center, -8, self.rect.bottom, self.weapon_type))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.animation()

    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >1000:
            self.last_update = now
            self.index = (self.index + 1) % len(self.images)  # Переключение на следующий костюм
            self.image = self.images[self.index]
