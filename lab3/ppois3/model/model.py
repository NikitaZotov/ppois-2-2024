from event import InitializeEvent, QuitEvent, TickEvent, StateChangeEvent, InputEvent, EatenEvent, EndLevelEvent, EndRunEvent, EndGameEvent, StartRunEvent
from event.event_manager import ev_manager
from model.map import Map
from .state import State
from .map_loader import MapLoader
from .state_machine import StateMachine
from config import config

from singleton import singleton


@singleton
class GameEngine:
    def __init__(
            self,
            state_machina: StateMachine,
            map_loader: MapLoader
    ):
        self.map_filename = r"resource/test.yaml"
        self.state = state_machina
        self.map_loader = map_loader
        self.ghost_manager = None
        self.map_: Map | None = None
        self.fruit_count = 0
        self.score = 0
        self.running = False
        self.end_run = False
        self.lives = config["lives"]

        ev_manager.add_handler(QuitEvent, lambda e: self.__quit_event_handler(e))
        ev_manager.add_handler(StateChangeEvent, lambda e: self.__change_state_event_handler(e))
        ev_manager.add_handler(InputEvent, lambda e: self.__input_event_handler(e))
        ev_manager.add_handler(EatenEvent, lambda e: self.__eaten_event_handler(e))
        ev_manager.add_handler(EndLevelEvent, self.__get_end_level_event_handler())
        ev_manager.add_handler(TickEvent, self.__get_tick_event_handler())
        ev_manager.add_handler(EndRunEvent, self.__get_end_run_event_handler())
        ev_manager.add_handler(EndGameEvent, self.__get_end_game_event_handler())

    def run(self):
        self.running = True
        ev_manager.notify(InitializeEvent())
        while self.running:
            new_tick = TickEvent()
            ev_manager.notify(new_tick)

    def __get_tick_event_handler(self):
        death_count = 66

        def handler(event: TickEvent):
            nonlocal death_count

            if self.end_run:
                death_count -= 1
                if death_count == 0:
                    death_count = 66
                    self.end_run = False
                    if self.map_:
                        self.map_.p_tracker.pacman.move(
                            self.map_.pacman_start_position - self.map_.p_tracker.pacman._position
                        )
                        self.map_.p_tracker.machibuse.move(
                            self.map_.machibuse_start_position - self.map_.p_tracker.machibuse._position
                        )
                        self.map_.p_tracker.machibuse.state_lock = False
                        self.map_.p_tracker.akabei.move(
                            self.map_.akabei_start_position - self.map_.p_tracker.akabei._position
                        )
                        self.map_.p_tracker.akabei.state_lock = False
                        self.map_.p_tracker.aosuke.move(
                            self.map_.aosuke_start_position - self.map_.p_tracker.aosuke._position
                        )
                        self.map_.p_tracker.aosuke.state_lock = False
                        self.map_.p_tracker.guzuta.move(
                            self.map_.guzuta_start_position - self.map_.p_tracker.guzuta._position
                        )
                        self.map_.p_tracker.guzuta.state_lock = False

                        self.map_.cookies_count -= self.map_.eaten_cookies_count
                        self.map_.eaten_cookies_count = 0
                        if self.lives <= -1:
                            ev_manager.notify(EndGameEvent())
                        else:
                            ev_manager.notify(StartRunEvent())
                            self.map_.p_tracker.pacman.move(
                                self.map_.pacman_start_position - self.map_.p_tracker.pacman._position
                            )

        return handler

    def __get_end_game_event_handler(self):
        state_machine = self.state

        def handler(event: EndGameEvent):
            nonlocal state_machine
            state_machine.push(State.enter_score)
            self.map_ = None

        return handler

    def __get_end_level_event_handler(self):
        state_machine = self.state

        def handler(event: EndLevelEvent):
            nonlocal state_machine
            state_machine.push(State.enter_score)

        return handler

    def __get_end_run_event_handler(self):
        def handler(event: EndRunEvent):
            self.end_run = True
            self.lives -= 1

        return handler

    def __quit_event_handler(self, event):
        self.running = False

    def __change_state_event_handler(self, event: StateChangeEvent):
        if not event.state:
            ev_manager.notify(QuitEvent())
        match event.state:
            case State.game_play:
                self.map_ = self.map_loader.load(self.map_filename)
                self.end_run = False
                self.score = 0
                self.fruit_count = 0
                ev_manager.notify(StartRunEvent())
        match event.prev_state:
            case State.game_play:
                self.map_ = None

    def __input_event_handler(self, event: InputEvent):
        match event.char:
            case 'esc':
                if self.state.peek() != State.game_play:
                    self.state.pop()
                else:
                    ev_manager.notify(QuitEvent())

    def __eaten_event_handler(self, event: EatenEvent):
        from .object import Cookie, Pacman, Powerup, Fruit, Ghost, Haste
        from event import EndLevelEvent
        from pygame import Vector2

        match event.game_object:
            case Cookie():
                self.score += config["cookie_price"]
                self.map_.remove(event.game_object)
                if self.map_.eaten_cookies_count in config["fruit_spawn"]:
                    self.map_.add(Fruit(Vector2(14, 20), self.fruit_count))
                    self.fruit_count += 1
                if self.map_.eaten_cookies_count == self.map_.cookies_count:
                    ev_manager.notify(EndRunEvent())
                    ev_manager.notify(EndLevelEvent())
            case Pacman():
                ev_manager.notify(EndRunEvent())
            case Powerup():
                self.score += config["powerup_price"]
                self.map_.remove(event.game_object)
            case Fruit():
                self.score += config["fruit_price"]*2**self.fruit_count
                self.map_.remove(event.game_object)
            case Haste():
                self.score += config["powerup_price"]
                self.map_.remove(event.game_object)
            case Ghost():
                self.score += config["ghost_price"]*2**self.fruit_count
                event.game_object.move(Vector2(13, 14) - event.game_object._position)


