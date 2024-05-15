import pygame
class BaseEnemy(pygame.sprite.Sprite):
	def __init__(self,x,y,enemy_data):
		super().__init__()
		self.image = pygame.image.load("../graphics/enemies/"+enemy_data.type+"/"+enemy_data.type+".png").convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))
		self.enemy_data = enemy_data


	def update(self, **kwargs):
		direction = kwargs.get('direction')
		self.rect.x += self.enemy_data.speed*direction


