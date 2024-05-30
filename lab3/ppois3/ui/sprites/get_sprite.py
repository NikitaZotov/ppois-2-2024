from model.object.ghosts import Akabei, Aosuke, Guzuta, Machibuse
from model.object.node import Node


def get_sprite(node: Node):

    from model.object import Pacman, Wall, Cookie, Powerup, Fruit, Haste
    from .spritesheet import SpriteSheet
    from .pacman_sprite import PacmanSprite
    from .wall_sprite import WallSprite
    from .cookie_sprite import CookieSprite
    from .powerup_sprite import PowerupSprite
    from .fruit_sprite import FruitSprite
    from .ghost_sprite import GhostSprite

    sprites_type = {
        Pacman: (PacmanSprite, SpriteSheet(
            r"resource/pacman.png",
            (32, 32),
            (32, 32)
        )),
        Wall: (WallSprite, SpriteSheet(
            r"resource/wall.png",
            (16, 16)
        )),
        Cookie: (CookieSprite, SpriteSheet(
            r"resource/cooky.png",
            (16, 16)
        )),
        Akabei: (GhostSprite, SpriteSheet(
            r"resource/ghost.png",
            (32, 32),
            (32, 32)
        )),
        Machibuse: (GhostSprite, SpriteSheet(
            r"resource/ghost.png",
            (32, 32),
            (32, 32)
        )),
        Aosuke: (GhostSprite, SpriteSheet(
            r"resource/ghost.png",
            (32, 32),
            (32, 32)
        )),
        Guzuta: (GhostSprite, SpriteSheet(
            r"resource/ghost.png",
            (32, 32),
            (32, 32)
        )),
        Powerup: (PowerupSprite, SpriteSheet(
            r"resource/powerup.png",
            (16, 16)
        )),
        Fruit: (FruitSprite, SpriteSheet(
            r"resource/fruit.png",
            (32, 32),
            (32, 32)
        )),
        Haste: (PowerupSprite, SpriteSheet(
            r"resource/haste.png",
            (16, 16)
        )),
    }

    if type(node) not in sprites_type:
        raise ValueError()

    sprite_type, sprite_sheet = sprites_type[type(node)]

    return sprite_type(node, sprite_sheet)
