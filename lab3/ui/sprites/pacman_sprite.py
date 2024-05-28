from .game_sprite import GameSprite


class PacmanSprite(GameSprite):
    def _get_sprite_indexer(self):
        from model.side import Side
        indexes = {
            Side.left: [0, 0, 6, 6, 0, 0, 4, 4],
            Side.right: [1, 1, 7, 7, 1, 1, 5, 5],
            Side.down: [2, 2, 8, 8, 2, 2, 4, 4],
            Side.up: [3, 3, 9, 9, 3, 3, 5, 5],
            Side.stop: [4]
        }
        death_animation = [x for x in range(13, 24)]
        count = 0
        death_count = 0
        was_dead = False

        def indexer():
            nonlocal count, indexes, death_animation, was_dead, death_count

            if not self._object.is_dead:
                sprites = indexes[self._object.direction]
                count = (count + 1) % len(sprites)
                return sprites[count]
            else:
                if not was_dead:
                    count = 0
                    was_dead = True
                death_count += 1
                if death_count == 6:
                    count = (count + 1)
                    death_count = 0
                if count == len(death_animation):
                    count = 0
                    was_dead = False
                    self._object.is_dead = False
                return death_animation[count]

        return indexer
