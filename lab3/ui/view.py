from abc import ABC, abstractmethod
from pygame import Surface
from pygame.sprite import Group
from model.model import GameEngine


class View(ABC):
    def __init__(self, parent_view, model: GameEngine):
        self.parent_view = parent_view
        self.model = model
        self._sprite_group = Group()
        self._build()

    @abstractmethod
    def _build(self):
        pass

    def kill(self):
        self._sprite_group.empty()

    def render(self, bg_color: int) -> Surface:
        menu_surface = Surface((self.parent_view.width, self.parent_view.height))
        menu_surface.fill(bg_color)
        self._sprite_group.update()
        self._sprite_group.draw(menu_surface)
        return menu_surface
