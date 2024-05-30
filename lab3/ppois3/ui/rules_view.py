from pygame import Rect, Surface
from pygame.font import Font
from config import Config
from model.state import State
from ui.sprites import TextObject, Header
from ui.view import View


class RulesView(View):
    def _build(self):
        config = Config()
        self._header = Header(Rect(0, 0, self.parent_view.width, 40),
                              config["header_color"],
                              TextObject(lambda: "Rules", config["hd_text_color"]))
        self._header.rect.center = (self.parent_view.width / 2, self.parent_view.height / 12)
        self._sprite_group.add(self._header)
        relative_y = self._header.rect.centery + self._header.rect.height / 1.5

        def get_y_with_padding():
            nonlocal relative_y
            relative_y += self._header.rect.height / 1.5
            return relative_y

        for line in config["rules"].split('\n'):
            text = TextObject(lambda l=line: l, font=Font(None, 32))
            text.rect.x = 20
            text.rect.y = get_y_with_padding()
            self._sprite_group.add(text)
        back_button = TextObject(
            lambda: "Press Esc to back", color=config["text_color"]
        )
        back_button.rect.center = (self.parent_view.width / 2, get_y_with_padding() + 50)
        self._sprite_group.add(back_button)

    def render(self, bg_color: int) -> Surface:
        return super().render(bg_color)

    def __get_button_rect(self, y: float) -> Rect:
        button_rect = Rect(0, 0, 150, 50)
        button_rect.center = (self.parent_view.width / 2, self.parent_view.height / 4)
        button_rect.y = y
        return button_rect

    def __back_button_click_handler(self):
        if self.model.state.peek() == State.rules:
            self.model.state.pop()

