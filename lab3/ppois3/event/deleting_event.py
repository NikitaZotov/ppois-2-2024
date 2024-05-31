from .event import Event


class DeletingEvent(Event):
    name = "Deleting event"

    def __init__(self, object_):
        self.object = object_
