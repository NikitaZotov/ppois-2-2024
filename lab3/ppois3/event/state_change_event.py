from .event import Event
from model.state import State


class StateChangeEvent(Event):
    name = "State change event"

    def __init__(
            self,
            state: State | None,
            prev_state: State
    ):
        self.state = state
        self.prev_state = prev_state
