from typing import Callable

from event import Event


class GhostStateEvent(Event):
    name = "ghost_state_event"

    def __init__(self, ghost_state: type | None = None, ghost: type | None = None):
        self.ghost_state = ghost_state
        self.ghost = ghost

    def __str__(self):
        return f"Ghost state event"