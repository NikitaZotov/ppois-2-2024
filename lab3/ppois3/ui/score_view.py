from pygame import Surface, Rect
import json
from config import Config
from model.state import State
from .sprites import TextObject, Header
from .view import View


class ScoreView(View):

    def _build(self):
        config = Config()
        self._header = Header(Rect(0, 0, self.parent_view.width, 45),
                              config["header_color"],
                              TextObject(lambda: "Scores", config["hd_text_color"]))
        self._header.rect.center = (self.parent_view.width / 2, self.parent_view.height / 12)
        self._sprite_group.add(self._header)
        self._relative_y = self._header.rect.y
        self.__get_scores()
        back_button = TextObject(
            lambda: "Press Esc to back", color=config["text_color"]
        )
        back_button.rect.center = (self.parent_view.width / 2, self.__get_relative_y()+50)
        self._sprite_group.add(back_button)

    def render(self, bg_color: int) -> Surface:
        return super().render(bg_color)

    def __back_button_click_handler(self):
        if self.model.state.peek() == State.score:
            self.model.state.pop()

    def __get_button_rect(self, y: float) -> Rect:
        button_rect = Rect(0, 0, 150, 50)
        button_rect.center = (self.parent_view.width / 2, self.parent_view.height / 4)
        button_rect.y = y
        return button_rect

    def __get_relative_y(self) -> int:
        self._relative_y += 75
        return self._relative_y

    def __get_scores(self):
        config = Config()
        with open(config["score_file_path"], 'r') as file:
            scores: dict[str, int] = json.loads(file.read())
        values = list(scores.values())
        values.sort()
        values.reverse()
        values_len = len(values)
        if values_len < 5:
            values.extend([0] * (5 - values_len))
        elif values_len > 5:
            while len(values) != 5:
                values.remove(values[-1])
        count = 0

        def get_str(int_score: int):
            if int_score >= 999999:
                return "999999"
            else:
                str_score = str(int_score)
                for i in range(6 - len(str_score)):
                    str_score = "0" + str_score
                return str_score

        for value in values:
            for score in scores:
                if scores[score] == value and count != values_len:
                    count += 1
                    score_text = TextObject(lambda v=score, s=scores[score]: f"{v} --- {get_str(s)}")
                    score_text.rect.center = self._header.rect.center
                    score_text.rect.y = self.__get_relative_y()
                    self._sprite_group.add(score_text)
            if value == 0:
                text = TextObject(lambda: "---")
                text.rect.center = self._header.rect.center
                text.rect.y = self.__get_relative_y()
                self._sprite_group.add(text)

