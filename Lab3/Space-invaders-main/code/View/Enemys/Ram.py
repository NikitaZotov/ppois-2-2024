import pygame
from Controller.ConfigurationManager import ConfigurationManager
from View.Enemys.BaseEnemy import BaseEnemy

class Ram(BaseEnemy):
	def __init__(self, x, y, enemy_data):
		super().__init__(x, y, enemy_data)
		self.ConfigurationManager = ConfigurationManager()
		self.images = self.ConfigurationManager.load_images("../graphics/enemies/ram")
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect(midbottom=(x,y))
		self.last_update = pygame.time.get_ticks()


	def update(self, **kwargs):
		self.rect.y += self.enemy_data.speed
		self.animation()

	def animation(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 400:
			self.last_update = now
			self.index = (self.index + 1) % len(self.images)
			self.image = self.images[self.index]

