from model.object import Crossroad
from model.object.ghosts import GhostState
from model.side import Side


class FinalState(GhostState):
    def _build(self):
        self._ghost.direction = Side.stop
        self._ghost.state_lock = True

    def on_crossroad_reached(self, node: Crossroad):
        self._ghost.direction = Side.stop