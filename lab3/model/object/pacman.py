from pygame import Vector2

from event.event_manager import ev_manager
from config import config
from model.side import Side
from event import TickEvent, InputEvent, EatenEvent

from .crossroad import Crossroad
from .game_object import GameObject


class Pacman(GameObject):
    name = "pacman"

    def __init__(
            self,
            node: Crossroad
    ):
        super().__init__(node._position.copy())
        self.node = node
        self.direction: Side = Side.stop
        self.next_direction = Side.stop
        self.tick_count = 0
        self.tile_time = config["pacman_tile_time"]
        self.is_dead = False
        self.is_hastened = False
        self.handlers = {
            TickEvent: self._get_tick_event_handler(),
            InputEvent: lambda e: self.__input_event_handler(e),
            EatenEvent: lambda e: self.__eaten_event_manager(e),
        }
        for event, handler in self.handlers.items():
            ev_manager.add_handler(event, handler)

    @property
    def position(self) -> Vector2:
        return self._position + self.direction.value * (self.tick_count / self.tile_time)

    def collision(self, node):
        from .ghosts.ghost import Ghost
        from event import EatenEvent

        match node:
            case Crossroad():
                self.__on_crossroad_reached(node)
            case _:
                if not isinstance(node, Ghost):
                    ev_manager.notify(EatenEvent(node))

    def kill(self):
        ev_manager.remove_handler(self.handlers.values())

    def _get_tick_event_handler(self):
        haste_time = config["haste_time"]

        def handler(event: TickEvent):
            nonlocal haste_time
            if self.is_dead:
                return
            if self.direction != Side.stop:
                self.tick_count += 1
                if self.is_hastened:
                    haste_time -= 1
                    self.tick_count += 1
                    if haste_time == 0:
                        haste_time = config["haste_time"]
                        self.is_hastened = False
                if self.tick_count == self.tile_time:
                    self.move(self.direction.value)
                    self.tick_count = 0

        return handler

    def __input_event_handler(self, event: InputEvent):
        if not event.char:
            return

        match event.char:
            case 'up arrow':
                self.next_direction = Side.up
            case 'right arrow':
                self.next_direction = Side.right
            case 'down arrow':
                self.next_direction = Side.down
            case 'left arrow':
                self.next_direction = Side.left

        if self.direction == Side.stop:
            self.__on_crossroad_reached(self.node)

        if self.next_direction == self.direction.reverse():
            if self.tick_count != 0:
                self.move(self.direction.value)
                self.tick_count = (self.tile_time - self.tick_count)
            self.direction = self.next_direction

    def __eaten_event_manager(self, event: EatenEvent):
        from .haste import Haste

        match event.game_object:
            case Pacman():
                self.is_dead = True
                self.direction = Side.stop
            case Haste():
                self.is_hastened = True

    def __on_crossroad_reached(self, node: Crossroad):
        from .ghosts.ghost_house import GhostHouse

        if node.adjacent_nodes[self.next_direction] and not isinstance(node.adjacent_nodes[self.next_direction],
                                                                       GhostHouse):
            self.direction = self.next_direction
        elif not node.adjacent_nodes[self.direction]:
            self.direction = Side.stop
        self.node = node
