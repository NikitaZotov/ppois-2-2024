from pygame import Rect

from config import config
from event import QuitEvent
from event.event_manager import ev_manager
from model.state import State
from .sprites import Button
from .sprites import TextObject
from .view import View


class MainMenuView(View):

    def _build(self):
        # noinspection PyTypeChecker
        self._sprite_group.add(
            Button(
                self.__get_push_state(State.game_play),
                TextObject(lambda: "Start", color=config["bt_text_color"]),
                rect=self.__get_button_rect(50), hover_color=config["bt_hover_color"]),
            Button(
                self.__get_push_state(State.settings),
                TextObject(lambda: "Settings", color=config["bt_text_color"]),
                rect=self.__get_button_rect(150), hover_color=config["bt_hover_color"]),
            Button(
                self.__get_push_state(State.score),
                TextObject(lambda: "Scores", color=config["bt_text_color"]),
                rect=self.__get_button_rect(250), hover_color=config["bt_hover_color"]),
            Button(
                self.__get_push_state(State.rules),
                TextObject(lambda: "Rules", color=config["bt_text_color"]),
                rect=self.__get_button_rect(350), hover_color=config["bt_hover_color"]),
            Button(
                self.__notify_quit,
                TextObject(lambda: "Exit", color=config["bt_text_color"]),
                rect=self.__get_button_rect(450), hover_color=config["bt_hover_color"]),
        )

    def __get_button_rect(self, y: float) -> Rect:
        button_rect = Rect(0, 0, 300, 50)
        button_rect.center = (self.parent_view.width / 2, self.parent_view.height / 5)
        button_rect.y = y
        return button_rect

    def __notify_quit(self):
        if self.model.state.peek() == State.main_menu:
            ev_manager.notify(QuitEvent())

    def __get_push_state(self, state):
        state_machine = self.model.state

        def push_settings_state():
            nonlocal state_machine
            if state_machine.peek() == State.main_menu:
                state_machine.push(state)

        return push_settings_state
