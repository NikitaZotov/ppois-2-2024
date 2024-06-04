import pygame.transform

from .game_sprite import GameSprite


class PowerupSprite(GameSprite):
    def _get_sprite_indexer(self):
        return lambda: 0
