import pygame
from pygame import Rect
from config import config
from event import InitializeEvent, QuitEvent, TickEvent, StateChangeEvent
from event.event_manager import ev_manager
from model.model import GameEngine
from model.state import State
from .gameplay_view import GameplayView
from .main_menu_view import MainMenuView
from .rules_view import RulesView
from .score_view import ScoreView
from .settings_view import SettingsView
from .view import View
from .enter_score_view import EnterScoreView


class GeneralViewManager:
    def __init__(self, model: GameEngine):
        self.model = model
        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.current_view: View | None = None
        self.state_views = None
        self.screen_width = config["width"]
        self.screen_height = config["height"]

        ev_manager.add_handler(InitializeEvent, lambda e: self.__init_event_handler(e))
        ev_manager.add_handler(QuitEvent, lambda e: self.__quit_event_handler(e))
        ev_manager.add_handler(TickEvent, lambda e: self.__tick_event_handler(e))
        ev_manager.add_handler(StateChangeEvent, lambda e: self.__state_change_event_handler(e))

    def initialize(self):
        pygame.font.init()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.current_view = MainMenuView(Rect(0, 0, self.screen_width, self.screen_height), self.model)
        self.is_initialized = True

    def __render_current_view(self):
        if not self.is_initialized:
            return
        self.screen.blit(self.current_view.render(config["bg_color"]), (0, 0))
        pygame.display.flip()

    def __init_event_handler(self, e):
        self.initialize()

    def __quit_event_handler(self, e):
        self.is_initialized = False
        pygame.quit()

    def __tick_event_handler(self, e):
        self.__render_current_view()
        self.clock.tick(config["fps"])

    def __state_change_event_handler(self, e):
        if not e.state:
            return

        state_views = {
            State.main_menu: MainMenuView,
            State.settings: SettingsView,
            State.game_play: GameplayView,
            State.score: ScoreView,
            State.rules: RulesView,
            State.enter_score: EnterScoreView
        }

        self.current_view.kill()
        self.current_view = state_views[e.state](Rect(0, 0, self.screen_width, self.screen_height), self.model)
