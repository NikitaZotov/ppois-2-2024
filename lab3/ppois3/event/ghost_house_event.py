from event import Event


class GhostHouseEvent(Event):
    name = "ghost_state_event"

    def __init__(self, ghost: type = None, state: type = None):
        self.ghost = ghost
        self.ghost_state = state

    def __str__(self):
        return "Ghost house event"