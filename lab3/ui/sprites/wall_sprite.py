import pygame.transform

from .game_sprite import GameSprite


class WallSprite(GameSprite):
    def _get_sprite_indexer(self):
        return lambda: self._object.type

    def update(self):
        GameSprite.update(self)
        self.image = pygame.transform.rotate(self.image, 90 * self._object.rotation)
