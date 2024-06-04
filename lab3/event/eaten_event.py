from .event import Event


class EatenEvent(Event):
    name = "Eaten event"

    def __init__(
            self,
            object_
    ):
        from model.object.node import Node
        self.game_object: Node = object_
