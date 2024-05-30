import pygame

from .game_sprite import GameSprite


class AkabeiSprite(GameSprite):
    def _get_sprite_indexer(self):
        from model.side import Side
        indexes = {
            Side.left: [0, 6, 0, 4],
            Side.right: [1, 7, 1, 5],
            Side.down: [2, 8, 2, 4],
            Side.up: [3, 9, 3, 5],
            Side.stop: [4]
        }
        count = 0

        def indexer():
            nonlocal count, indexes
            sprites = indexes[self._object.direction]
            count = (count + 1) % len(sprites)
            return sprites[count]

        return indexer

    def update(self):
        GameSprite.update(self)
        self.image.fill((255, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
