import random


class Util:
    @staticmethod
    def get_spawn_coordinates(window_width, window_height):
        border = random.choice(["top", "right", "bottom", "left"])

        if border == "top":
            x = random.randint(0, window_width)
            y = 0
        elif border == "right":
            x = window_width
            y = random.randint(0, window_height)
        elif border == "bottom":
            x = random.randint(0, window_width)
            y = window_height
        else:  # "left"
            x = 0
            y = random.randint(0, window_height)
        return x, y

    @staticmethod
    def is_point_in_square(x, y, enemy):
        return (x <= enemy.x + enemy.size / 2) and (x >= enemy.x - enemy.size / 2) and (
                y <= enemy.y + enemy.size / 2) and (y >= enemy.y - enemy.size / 2)

    @staticmethod
    def if_the_enemy_is_near(player, enemy):
        return Util.is_point_in_square(player.x - player.size / 3, player.y - player.size / 3,
                                       enemy) or Util.is_point_in_square(player.x + player.size / 3,
                                                                         player.y - player.size / 3,
                                                                         enemy) or Util.is_point_in_square(
            player.x - player.size / 3, player.y + player.size / 3, enemy) or Util.is_point_in_square(
            player.x + player.size / 3, player.y + player.size / 3, enemy)
