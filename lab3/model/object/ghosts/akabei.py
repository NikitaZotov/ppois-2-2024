from pygame import Vector2
from event.event_manager import ev_manager
from . import Ghost
from config import config


class Akabei(Ghost):
    name = "akabei"
    type = 0

    def _build(self):
        from event import GhostStateEvent
        self._scatter_target_position = Vector2(config["m1_aka_scatter_pos"][0], config["m1_aka_scatter_pos"][1])
        self._cruise_elroy = False
        ev_manager.add_handler(GhostStateEvent, lambda e: self.__change_state_event_handler(e))

    def __change_state_event_handler(self, e):
        from . import ScatterState, ChaseState, FrightState, CruiseElroyState, FinalState
        if not e.ghost:
            if e.ghost_state is ScatterState and not self._cruise_elroy:
                self._change_state(e.ghost_state(self, self._scatter_target_position))
            elif e.ghost_state is ChaseState:
                self._change_state(e.ghost_state(self))
            elif e.ghost_state is FrightState:
                self._change_state(e.ghost_state(self))
            elif e.ghost_state is CruiseElroyState:
                self._cruise_elroy = True
                self.tile_time -= 1
            elif e.ghost_state is FinalState:
                self._change_state(e.ghost_state(self))

