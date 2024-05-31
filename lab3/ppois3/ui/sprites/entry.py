from pygame.sprite import Sprite

from event.event_manager import ev_manager
from event import InputEvent

from .text_object import TextObject


class Entry(Sprite):
    def __init__(
            self,
            char_limit: int | None = None
    ):
        Sprite.__init__(self)
        self.content = ""
        self._text_object = TextObject(
            lambda: self.content
        )
        self.image = self._text_object.image
        self.char_limit = char_limit
        self.rect = self._text_object.rect

        ev_manager.add_handler(InputEvent, self.__get_input_event_manager())

    def update(self, *args, **kwargs):
        self._text_object.update()
        self.image = self._text_object.image
        self.rect = self._text_object.rect

    def __get_input_event_manager(self):
        def handler(event: InputEvent):
            if not event.char:
                return
            if event.char == "backspace":
                if self.content != "":
                    self.content = self.content[:-1]
            if len(self.content) >= self.char_limit:
                return
            if len(event.char) == 1:
                self.content += event.char

        return handler
