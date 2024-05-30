import pygame.mixer
from pygame import Surface, Rect

from config import config
from .sprites import TextObject, Button, Header
from .view import View


class SettingsView(View):
    def _build(self):

        header = Header(Rect(0, 0, self.parent_view.width, 75),
                        config["header_color"],
                        TextObject(lambda: "Settings", config["hd_text_color"]))
        header.rect.center = (self.parent_view.width / 2, self.parent_view.height / 7)

        music_button = Button(
            *self.__get_music_pause_on_click(),
            rect=Rect(0, 0, 240, 60),
            hover_color=config["bt_hover_color"]
        )
        music_button.rect.center = (self.parent_view.width / 3, self.parent_view.height / 2)

        map_button = Button(
            *self.__get_map_change_on_click(),
            rect=Rect(0, 0, 240, 60),
            hover_color=config["bt_hover_color"]
        )
        map_button.rect.center = (self.parent_view.width / 3 * 2, self.parent_view.height / 2)

        back_button = TextObject(
                lambda: "Press Esc to back", color=config["text_color"]
            )
        back_button.rect.center = (self.parent_view.width / 2, self.parent_view.height - 60)

        self._sprite_group.add(
            music_button,
            map_button,
            back_button,
            header
        )

    def render(self, bg_color: int) -> Surface:
        return super().render(bg_color)

    def __get_music_pause_on_click(self):
        paused = False

        def on_click():
            nonlocal paused
            if paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            paused = not paused

        return on_click, TextObject(
            lambda: "Off/On music",
            config["bt_text_color"]
        )

    def __get_map_change_on_click(self):
        paused = self.model.map_filename != r"resource/test.yaml"
        model = self.model

        def on_click():
            nonlocal paused, model
            if paused:
                model.map_filename = r"resource/test.yaml"
            else:
                model.map_filename = r"resource/test1.yaml"
            paused = not paused

        return on_click, TextObject(
            lambda: "Map 1" if not paused else "Map 2",
            config["bt_text_color"]
        )

    def __back_button_click_handler(self):
        pass
