import pygame.font
from pygame.font import Font
from pygame.sprite import Sprite

from config import config

pygame.font.init()


class TextObject(Sprite):
    def __init__(
            self,
            text_func,
            color: int = config["text_color"],
            font: Font = Font(None, 50)
    ):
        super().__init__()
        self.text_func = text_func
        self.color = color
        self.font = font
        self.image = self._render_text()
        self.rect = self.image.get_rect()

    def _render_text(self):
        return self.font.render(
            self.text_func(),
            False,
            self.color
        )

    def update(self):
        self.image = self._render_text()
        self.rect = self.image.get_rect(center=self.rect.center)
        if config["show_colliders"] == 1:
            pygame.draw.rect(self.image, config["collider_color"], self.image.get_rect(), 5)
