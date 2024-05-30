from pygame import Vector2

from config import config
from event import TickEvent
from event.event_manager import ev_manager
from . import GhostState


class ChaseState(GhostState):
    def _build(self):
        ev_manager.add_handler(TickEvent, lambda e: self.__tick_event_handler(e))
        self.p_tracker = self._ghost.p_tracker

    def __tick_event_handler(self, e):
        from . import Akabei, Machibuse, Aosuke, Guzuta

        if isinstance(self._ghost, Akabei):
            self.target_position = self.p_tracker.pacman_position
        elif isinstance(self._ghost, Machibuse):
            self.target_position = self.__get_machibuse_position()
        elif isinstance(self._ghost, Aosuke):
            self.target_position = self.__get_aosuke_position()
        elif isinstance(self._ghost, Guzuta):
            self.target_position = self.__get_guzuta_position()

    def __get_machibuse_position(self):
        from .ghost_house import GhostHouse

        pos = self.p_tracker.pacman_position + self.p_tracker.pacman.direction.value * 4
        return Vector2(config["m1_house_exit_pos"][0],
                       config["m1_house_exit_pos"][1]) if isinstance(self._ghost._node, GhostHouse) else pos

    def __get_aosuke_position(self):
        pac_pos = self.p_tracker.pacman_position + self.p_tracker.pacman.direction.value * 2
        return 2 * pac_pos - self.p_tracker.akabei_position

    def __get_guzuta_position(self):
        if self.p_tracker.pacman_position.distance_to(self._ghost.position) >= 8:
            return self.p_tracker.pacman_position
        else:
            return self._ghost._scatter_target_position
