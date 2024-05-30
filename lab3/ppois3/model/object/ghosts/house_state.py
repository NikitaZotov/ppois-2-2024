from event.event_manager import ev_manager
from model.side import Side
from . import GhostState
from .ghost_house import GhostHouse
from .. import Crossroad
from ..node import Node


class HouseState(GhostState):
    def _build(self):
        from event import GhostHouseEvent
        self._house_lock = True
        self._next_state = None
        ev_manager.add_handler(GhostHouseEvent, lambda e: self.__house_event_handler(e))

    def on_crossroad_reached(self, node: Crossroad):
        from event import GhostStateEvent
        min_dist = 999999999
        next_direction = Side.stop
        for direction in Side:
            if direction == Side.stop or direction == self._ghost.direction.reverse():
                continue
            adj_node = node.adjacent_nodes[direction]
            if isinstance(adj_node, Node):
                if not isinstance(adj_node, GhostHouse):
                    self._house_lock = True
                elif isinstance(adj_node, GhostHouse) and self._house_lock:
                    continue
                if (dist := adj_node.position.distance_to(self.target_position)) < min_dist:
                    min_dist = dist
                    next_direction = direction

        self._ghost.direction = next_direction
        if node.position == self.target_position and self._next_state:
            self._ghost._house_lock = False
            ev_manager.notify(GhostStateEvent(self._next_state, type(self._ghost)))

    def __house_event_handler(self, e):
        if e.ghost_state and e.ghost is type(self._ghost):
            self._house_lock = False
            self._next_state = e.ghost_state