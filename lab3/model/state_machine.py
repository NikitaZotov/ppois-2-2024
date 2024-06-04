from .state import State
from event.event_manager import EventManager
from event import StateChangeEvent


class StateMachine:
    def __init__(self):
        self._stack = [State.main_menu]

    def push(self, state: State) -> None:
        EventManager().notify(
            StateChangeEvent(
                state,
                self.peek(),
            )
        )
        self._stack.append(state)

    def pop(self) -> State:
        state = self._stack.pop()
        EventManager().notify(
            StateChangeEvent(
                self.peek(),
                state,
            )
        )
        return state

    def peek(self):
        return self._stack[-1] if self._stack else None
