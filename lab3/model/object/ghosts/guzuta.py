from pygame import Vector2

from config import config
from event.event_manager import ev_manager
from . import Ghost


class Guzuta(Ghost):
    name = "guzuta"
    type = 3

    def _build(self):
        from event import GhostStateEvent, GhostHouseEvent
        self._scatter_target_position = Vector2(config["m1_guzu_scatter_pos"][0], config["m1_guzu_scatter_pos"][1])
        self._house_lock = False
        ev_manager.add_handler(GhostStateEvent, lambda e: self.__change_state_event_handler(e))
        ev_manager.add_handler(GhostHouseEvent, lambda e: self.__house_event_handler(e))

    def __change_state_event_handler(self, e):
        from . import ScatterState, ChaseState, FrightState, FinalState
        if not e.ghost or e.ghost is Guzuta:
            if e.ghost_state is FinalState:
                self._change_state(e.ghost_state(self))
            if not self._house_lock:
                if e.ghost_state is ScatterState:
                    self._change_state(e.ghost_state(self, self._scatter_target_position))
                elif e.ghost_state is ChaseState:
                    self._change_state(e.ghost_state(self))
                elif e.ghost_state is FrightState:
                    self._change_state(e.ghost_state(self))

    def __house_event_handler(self, e):
        if e.ghost is Guzuta:
            from . import HouseState
            if not self._house_lock:
                self._house_lock = True
            if self._house_lock:
                self._change_state(HouseState(self, Vector2(config["m1_house_exit_pos"][0],
                                                            config["m1_house_exit_pos"][1])))
