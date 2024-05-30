from config import config
from utils import add_score

from .view import View


class EnterScoreView(View):

    def _build(self):
        from .sprites import TextObject, Entry, Button

        label = TextObject(
            lambda: "Enter name"
        )
        label.rect.center = (self.parent_view.width / 2, self.parent_view.height / 2 - 50)

        self.entry = Entry(char_limit=30)
        self.entry.rect.center = (self.parent_view.width / 2, self.parent_view.height / 2)
        from pygame import Rect
        button = Button(
            self.__get_on_click(),
            TextObject(
                lambda: "OK",
                config["bt_text_color"]
            ),
            rect=Rect(
                0,
                0,
                200,
                50
            ),
            hover_color=config["bt_hover_color"]
        )

        button.rect.center = (self.parent_view.width / 2, self.parent_view.height - 100)

        self._sprite_group.add(
            label,
            self.entry,
            button
        )

    def __get_on_click(self):
        from event.event_manager import ev_manager
        from event import QuitEvent
        entry = self.entry
        model = self.model

        def on_click():
            nonlocal entry, model
            if entry.content == "":
                return
            add_score(entry.content, model.score)
            ev_manager.notify(QuitEvent())

        return on_click
