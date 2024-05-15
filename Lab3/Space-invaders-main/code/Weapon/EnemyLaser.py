import pygame 
from Weapon.laser import Laser


class EnemyLaser(Laser):
	def __init__(self,pos,speed,screen_height):
		super().__init__(pos,speed,screen_height)

	def collision_with_player(self,player):
		if pygame.sprite.spritecollide(self, player, False):
			self.kill()
			for player_sprite in player:
				player_sprite.lives -= 1

	def update(self,blocks_group, player):
		self.rect.y += self.speed
		self.collision_with_blocks(blocks_group)
		self.collision_with_player(player)
		self.destroy()
