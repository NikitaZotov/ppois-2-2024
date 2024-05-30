from abc import ABC, abstractmethod

from pygame import Vector2

from model.side import Side
from .ghost_house import GhostHouse
from .. import Crossroad


class GhostState(ABC):
    def __init__(self, ghost, target_position: Vector2 = Vector2(0, 0)):
        self._ghost = ghost
        self._house_lock = False
        self.target_position = target_position
        self._build()

    @abstractmethod
    def _build(self):
        pass

    def on_crossroad_reached(self, node: Crossroad):
        min_dist = 999999999
        next_direction = Side.stop
        for direction in Side:
            if direction == Side.stop or direction == self._ghost.direction.reverse():
                continue
            adj_node = node.adjacent_nodes[direction]
            if isinstance(adj_node, Crossroad):
                if not isinstance(adj_node, GhostHouse):
                    self._house_lock = True
                elif isinstance(adj_node, GhostHouse) and self._house_lock:
                    continue
                if (dist := adj_node.position.distance_to(self.target_position)) < min_dist:
                    min_dist = dist
                    next_direction = direction
        self._ghost._node = node
        self._ghost.direction = next_direction

