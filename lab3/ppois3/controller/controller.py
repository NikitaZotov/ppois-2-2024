import pygame
from event import TickEvent, QuitEvent, InputEvent
from event.hover_event import HoverEvent
from event.event_manager import ev_manager
from model import GameEngine


class Controller:
    keys = {
        pygame.K_ESCAPE: "esc",
        pygame.K_UP: 'up arrow',
        pygame.K_RIGHT: 'right arrow',
        pygame.K_DOWN: 'down arrow',
        pygame.K_LEFT: 'left arrow',
        pygame.K_SPACE: 'space',
        pygame.K_BACKSPACE: 'backspace'
    }

    def __init__(self, model: GameEngine):
        self.model = model

        ev_manager.add_handler(TickEvent, lambda e: self._tick_event_handler(e))

    def _tick_event_handler(self, event):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    ev_manager.notify(QuitEvent())
                case pygame.KEYDOWN:
                    ev_manager.notify(
                        InputEvent(
                            self.keys[event.key] if event.key in self.keys else event.unicode,
                            None
                        )
                    )
                case pygame.MOUSEBUTTONDOWN:
                    ev_manager.notify(InputEvent(None, event.pos))
                case pygame.MOUSEMOTION:
                    ev_manager.notify(HoverEvent(event.pos))

