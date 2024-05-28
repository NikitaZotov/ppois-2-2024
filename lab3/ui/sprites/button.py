from typing import Callable
import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group

from config import Config
from event import InputEvent
from event import HoverEvent
from event.event_manager import ev_manager

config = Config()


class Button(Sprite):

    def __init__(
            self,
            on_click: Callable[[], None],
            *content_sprites,
            rect: Rect = Rect(0, 0, 100, 100),
            color: int = config["button_color"],
            hover_color: int | None = None
    ):
        super().__init__()
        self.rect = rect
        self.color = color
        self.image = None
        self.group = Group()
        if content_sprites:
            self.group.add(*map(self.__set_rect_center, content_sprites))
        self.bg_surface = self.__form_bg_surface(color)
        self.on_click = on_click

        ev_manager.add_handler(InputEvent, self.__get_mouse_click_input_event_handler())
        if hover_color:
            ev_manager.add_handler(HoverEvent, self.__get_mouse_hover_event_handler(hover_color))

    def update(self):
        self.group.update()
        self.image = self.bg_surface.copy()
        self.group.draw(self.image)
        if config["show_colliders"] == 1:
            pygame.draw.rect(self.image, config["collider_color"], self.image.get_rect(), 5)

    def __get_mouse_click_input_event_handler(self):
        rect = self.rect
        on_click = self.on_click

        def handler(event: InputEvent):
            nonlocal rect, on_click
            if event.click_pos:
                if rect.collidepoint(*event.click_pos):
                    on_click()

        return handler

    def __get_mouse_hover_event_handler(self,  hover_color: int):
        rect = self.rect

        def handler(e: HoverEvent):
            nonlocal rect
            if e.mouse_pos:
                if rect.collidepoint(*e.mouse_pos):
                    self.bg_surface = self.__form_bg_surface(hover_color)
                    self.update()
                else:
                    self.bg_surface = self.__form_bg_surface(self.color)
                    self.update()
        return handler

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