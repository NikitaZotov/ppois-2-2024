import pygame.draw
from pygame import Surface, Vector2
from pygame.sprite import Sprite, Group

from model.model import Map
from config import config
from event import DeletingEvent


class MapSprite(Sprite):
    def __init__(
            self,
            _map: Map,
            position: Vector2 = Vector2(0, 0)
    ):
        super().__init__()
        self._map = _map
        self.bg = config["map_background_view"]
        self.image = Surface((_map.width * config["tile_width"], _map.height * config["tile_height"]))
        self.sprites = Group()
        self.rect = self.image.get_rect(center=position)

        self._map.on_adding = self.__get_on_adding()

        from .get_sprite import get_sprite

        for object_ in self._map:
            try:
                sprite = get_sprite(object_)
                self.sprites.add(sprite)
            except ValueError:
                continue

        from event.event_manager import ev_manager
        ev_manager.add_handler(DeletingEvent, self.__get_deleting_event_handler())

    def update(self):
        self.sprites.update()
        self.image.fill(self.bg)
        self.sprites.draw(self.image)
        if config["show_colliders"] == 1:
            pygame.draw.rect(self.image, int(config["collider_color"], 16), self.image.get_rect(), 5)

    def __get_on_adding(self):
        group = self.sprites

        def on_adding(node):
            from .get_sprite import get_sprite
            nonlocal group
            group.add(get_sprite(node))

        return on_adding

    def __get_deleting_event_handler(self):
        group = self.sprites

        def handler(event: DeletingEvent):
            nonlocal group
            for sprite in group:
                if sprite._object is event.object:
                    sprite.kill()

        return handler
