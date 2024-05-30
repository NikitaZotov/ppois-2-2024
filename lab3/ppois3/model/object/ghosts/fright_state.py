import random

from config import config
from model.side import Side
from . import GhostState
from .ghost_house import GhostHouse
from .. import Crossroad
from ..node import Node


class FrightState(GhostState):
    def _build(self):
        self._ghost.tile_time = config["ghost_f_tile_time"]

    def on_crossroad_reached(self, node: Crossroad):
        next_directions = []
        for direction in Side:
            if direction == Side.stop:
                continue
            adj_node = node.adjacent_nodes[direction]
            if isinstance(adj_node, Node) and not isinstance(adj_node, GhostHouse):
                next_directions.append(direction)
        next_dir = dict(enumerate(next_directions))[random.randrange(0, len(next_directions))] \
            if len(next_directions) > 0 else Side.stop
        if next_dir == self._ghost.direction.reverse():
            if self._ghost.tick_count != 0:
                self._ghost.move(self._ghost.direction.value)
                self._ghost.direction = next_dir
                self._ghost.tick_count = (self._ghost.tile_time - self._ghost.tick_count)
            else:
                self._ghost.direction = next_dir
        else:
            self._ghost.direction = next_dir
        self._ghost._node = node