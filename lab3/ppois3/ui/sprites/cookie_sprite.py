from .game_sprite import GameSprite


class CookieSprite(GameSprite):
    def _get_sprite_indexer(self):
        return lambda: 0
