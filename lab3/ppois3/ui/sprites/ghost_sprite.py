from .game_sprite import GameSprite


class GhostSprite(GameSprite):
    def _get_sprite_indexer(self):
        object_ = self._object

        def indexer():
            from model.side import Side
            from model.object.ghosts import FrightState
            nonlocal object_

            directions = {
                Side.up: 0,
                Side.down: 1,
                Side.left: 2,
                Side.right: 3,
                Side.stop: 0
            }
            if isinstance(object_.state, FrightState):
                return 5
            return object_.type + directions[object_.direction] * 6

        return indexer
