from .game_sprite import GameSprite


class FruitSprite(GameSprite):
    def _get_sprite_indexer(self):
        return lambda: self._object.type
