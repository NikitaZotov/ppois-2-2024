from View.Enemys.BaseEnemy import BaseEnemy
from settings import screen_width
from random import choice

class Minion(BaseEnemy):
	def __init__(self, x, y, enemy_data):
		super().__init__(x, y, enemy_data)
		self.direction =  choice([-1, 1])


	def update(self, **kwargs):
		if self.rect.x <= 0 or self.rect.x >= screen_width:
			self.direction*=-1
		self.rect.x += self.direction*self.enemy_data.speed