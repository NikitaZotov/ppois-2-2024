from .event import Event


class CollisionEvent(Event):
    name = "Collision event"

    def __init__(
            self,
            game_object,
            other
    ):
        self.game_object = game_object
        self.other = other
