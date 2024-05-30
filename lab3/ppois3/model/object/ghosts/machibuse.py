from pygame import Vector2

from config import config
from event.event_manager import ev_manager
from . import Ghost


class Machibuse(Ghost):
    name = "machibuse"
    type = 1

    def _build(self):
        from event import GhostStateEvent
        self._scatter_target_position = Vector2(config["m1_machi_scatter_pos"][0], config["m1_machi_scatter_pos"][1])
        ev_manager.add_handler(GhostStateEvent, lambda e: self.__change_state_event_handler(e))

    def __change_state_event_handler(self, e):
        from . import ScatterState, ChaseState, FrightState, FinalState
        if not e.ghost:
            if e.ghost_state is ScatterState:
                self._change_state(e.ghost_state(self, self._scatter_target_position))
            elif e.ghost_state is ChaseState:
                self._change_state(e.ghost_state(self))
            elif e.ghost_state is FrightState:
                self._change_state(e.ghost_state(self))
            elif e.ghost_state is FinalState:
                self._change_state(e.ghost_state(self))