from abc import abstractmethod

from pygame import Vector2
from event.event_manager import ev_manager
from config import config
from model.side import Side
from event import TickEvent
from ..game_object import GameObject
from .. import Crossroad


class Ghost(GameObject):
    name = "ghost"
    type = -1

    def __init__(
            self,
            map_,
            position: Vector2 = Vector2(0, 0)
    ):
        super().__init__(position)
        self.state = None
        self.direction: Side = Side.stop
        self.tick_count = 0
        self.tile_time = config["ghost_tile_time"]
        self.p_tracker = map_.p_tracker
        self.state_lock = False
        self._node: Crossroad | None = None
        self._build()

        ev_manager.add_handler(TickEvent, lambda e: self.__tick_event_handler(e))

    @property
    def position(self) -> Vector2:
        return self._position + self.direction.value * (self.tick_count / self.tile_time)

    @abstractmethod
    def _build(self):
        pass

    def collision(self, node):
        match node:
            case Crossroad():
                self.state.on_crossroad_reached(node)

    def __tick_event_handler(self, event: TickEvent):
        from event import EatenEvent
        from model.object.ghosts import FrightState, ChaseState

        if self.p_tracker.pacman.is_dead:
            return

        self.tick_count = (self.tick_count + 1) % self.tile_time
        if self.tick_count == 0:
            self.move(self.direction.value)
        if ((self.position - self.p_tracker.pacman_position).length() <=
                (0.5 if not self.p_tracker.pacman.is_hastened else 0.5)):
            if not isinstance(self.state, FrightState):
                ev_manager.notify(EatenEvent(self.p_tracker.pacman))
        if ((self.p_tracker.pacman_position - self.position).length() <=
                (0.5 if not self.p_tracker.pacman.is_hastened else 0.5)):
            if isinstance(self.state, FrightState):
                ev_manager.notify(EatenEvent(self))
                self.state = ChaseState(self)

    def _change_state(self, state):
        from . import GhostState, FrightState, HouseState
        if not self.state_lock:
            self.state: GhostState = state
            if not isinstance(state, FrightState | HouseState):
                if self.tile_time != config["ghost_tile_time"]:
                    self.tile_time = config["ghost_tile_time"]
                else:
                    if self._node and self.position == self._node.position:
                        if self._node.adjacent_nodes[self.direction.reverse()]:
                            if self.tick_count != 0:
                                self._position += self.direction.value
                                self.tick_count = (self.tile_time - self.tick_count)
                            self.direction = self.direction.reverse()
                    else:
                        if self.tick_count != 0:
                            self._position += self.direction.value
                            self.tick_count = (self.tile_time - self.tick_count)
                        self.direction = self.direction.reverse()

    def __get_direction(self) -> Side:
        position1 = self._position
        position2 = self.state.target_position
        if position2.x > position1.x:
            return Side.right
        elif position2.x < position1.x:
            return Side.left
