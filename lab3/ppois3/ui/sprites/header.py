import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group

from config import Config

config = Config()


class Header(Sprite):

    def __init__(self,
                 rect: Rect = Rect(0, 0, 100, 100),
                 header_color: int = config["default_color"],
                 *content_sprites):
        super().__init__()
        self.rect = rect
        self.header_color = header_color
        self.content_sprites = content_sprites
        self.image = None
        self.group = Group()
        if content_sprites:
            self.group.add(*map(self.__set_rect_center, content_sprites))
        self.bg_surface = self.__form_bg_surface(header_color)

    def update(self):
        self.group.update()
        self.image = self.bg_surface.copy()
        self.group.draw(self.image)
        if config["show_colliders"] == 1:
            pygame.draw.rect(self.image, config["collider_color"], self.image.get_rect(), 5)

    def __form_bg_surface(self, color: int) -> Surface:
        sc = Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(sc, color, (0, 0, self.rect.width, self.rect.height))
        return sc

    def __set_rect_center(self, content_sprite):
        content_sprite.rect.center = (
            self.rect.width / 2,
            self.rect.height / 2,
        )
        return content_sprite