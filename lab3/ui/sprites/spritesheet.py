from os import PathLike

import pygame.image

from config import config


class SpriteSheet:
    def __init__(
            self,
            filename: str | bytes | PathLike,
            image_size: (int, int) = (config["image_width"], config["image_height"]),
            tile_size: (int, int) = (config["tile_width"], config["tile_height"])
    ):
        image = pygame.image.load(filename)
        self.line_size = image.get_width() // image_size[0]
        self.image = pygame.transform.scale(
            image,
            (
                image.get_width() * (tile_size[0] / image_size[0]),
                image.get_height() * (tile_size[1] / image_size[1])
            )
        )
        self.pattern = pygame.rect.Rect(0, 0, *tile_size)

    def get_image(self, index: int):
        x = (index % self.line_size) * self.pattern.width
        y = (index // self.line_size) * self.pattern.height
        self.image.set_clip(self.pattern.move(x, y))
        return self.image.subsurface(self.image.get_clip())

    def __getitem__(self, item: int):
        return self.get_image(item)
