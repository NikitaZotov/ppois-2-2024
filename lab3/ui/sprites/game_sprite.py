from abc import ABC, abstractmethod

import pygame.draw
from pygame import Surface, Rect
from pygame.sprite import Sprite

from config import config
from .spritesheet import SpriteSheet


class GameSprite(Sprite, ABC):
    from model.object.node import Node

    show_collider = config["show_colliders"] == 1
    collider_color = config["collider_color"]

    def __init__(
            self,
            _object: Node,
            sprite_sheet: SpriteSheet | None
    ):
        super().__init__()
        self._object = _object
        self.sprite_sheet = sprite_sheet
        self.sprite_indexer = self._get_sprite_indexer()
        self.image: Surface = sprite_sheet[0] if sprite_sheet else None
        self.rect: Rect = self.image.get_rect(
            topleft=_object.position*config["tile_width"]
        ) if self.image else None

    def update(self):
        from pygame import Vector2
        self.rect.center = (self._object.position + Vector2(0.5, 0.5))*config["tile_width"]
        self.image = self.sprite_sheet[self.sprite_indexer()]
        if not self.image:
            return
        if self.show_collider:
            pygame.draw.rect(
                self.image,
                self.collider_color,
                self.image.get_rect(),
                1
            )

    @abstractmethod
    def _get_sprite_indexer(self): pass

