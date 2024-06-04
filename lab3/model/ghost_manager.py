from event import TickEvent, GhostStateEvent, EatenEvent, GhostHouseEvent, EndRunEvent, StartRunEvent
from event.event_manager import ev_manager
from model import GameEngine
from .object import Powerup
from .object.ghosts import ScatterState, ChaseState, CruiseElroyState, FrightState, FinalState
from .object.ghosts.aosuke import Aosuke
from .object.ghosts.guzuta import Guzuta


class ChangeStateEvent:
    pass


class GhostManager:
    def __init__(self, model: GameEngine):
        self.ghosts = []
        self.model = model
        self.ticks = 0
        self.seconds_passed = 0
        self.total_seconds_passed = 0
        self.chase_flag = False
        self.clock_pause = False
        self.current_wave = False
        self.lock = True

        self.handlers = (
            lambda e: self.__handle_tick_event(e),
            lambda e: self.__handle_initialize_event(e),
            lambda e: self.__handle_eaten_event(e),
            lambda e: self.__handle_end_run_event(e)
        )

        ev_manager.add_handler(TickEvent, self.handlers[0])
        ev_manager.add_handler(StartRunEvent, self.handlers[1])
        ev_manager.add_handler(EatenEvent, self.handlers[2])
        ev_manager.add_handler(EndRunEvent, self.handlers[3])

    def kill(self):
        ev_manager.remove_handler(self.handlers)

    def __handle_tick_event(self, e):
        if not self.lock:
            self.__tick_clock(self.clock_pause)
            self.__change_wave() if not self.clock_pause else self.__fright_wave()

    def __handle_initialize_event(self, e):
        self.lock = False
        ev_manager.notify(GhostStateEvent(ScatterState if not self.chase_flag else ChaseState))
        ev_manager.notify(GhostHouseEvent(Aosuke))
        ev_manager.notify(GhostHouseEvent(Guzuta))
        self.current_wave = ScatterState

    def __change_wave(self):
        match (self.seconds_passed, self.chase_flag):
            case (7, False):
                if self.total_seconds_passed <= 54:
                    self.chase_flag = True
                    self.seconds_passed = 0
                    ev_manager.notify(GhostStateEvent(ChaseState))
                    self.current_wave = ChaseState
            case (5, False):
                if self.total_seconds_passed > 54:
                    self.chase_flag = True
                    self.seconds_passed = 0
                    ev_manager.notify(GhostStateEvent(ChaseState))
                    self.current_wave = ChaseState
            case (20, True):
                if self.total_seconds_passed <= 84:
                    self.seconds_passed = 0
                    self.chase_flag = False
                    ev_manager.notify(GhostStateEvent(ScatterState))
                    self.current_wave = ScatterState

    def __handle_eaten_event(self, e):
        if self.model.map_:
            if isinstance(e.game_object, Powerup):
                ev_manager.notify(GhostStateEvent(FrightState))
                self.clock_pause = True
                self.seconds_passed = 0
                self.current_wave = ChaseState if self.chase_flag else ScatterState
            if (self.model.map_.cookies_count - self.model.map_.eaten_cookies_count == 20
                    or self.model.map_.cookies_count - self.model.map_.eaten_cookies_count == 10):
                ev_manager.notify(GhostStateEvent(CruiseElroyState))
            if self.model.map_.eaten_cookies_count == 30 if self.model.map_.cookies_count > 30 else 1:
                ev_manager.notify(GhostHouseEvent(Aosuke, self.current_wave))
            if self.model.map_.eaten_cookies_count == self.model.map_.cookies_count // 3:
                ev_manager.notify(GhostHouseEvent(Guzuta, self.current_wave))

    def __tick_clock(self, clock_pause: bool):
        self.ticks += 1
        if self.ticks == 30:
            self.seconds_passed += 1
            self.total_seconds_passed += 1 if not clock_pause else 0
            self.ticks = 0

    def __fright_wave(self):
        if self.seconds_passed == 6:
            ev_manager.notify(GhostStateEvent(changed := (ChaseState if self.chase_flag else ScatterState)))
            self.current_wave = changed
            self.seconds_passed = 0
            self.clock_pause = False

    def __handle_end_run_event(self, e):
        ev_manager.notify(GhostStateEvent(FinalState))

