from event import Event


class HoverEvent(Event):
    name = "Hover event"

    def __init__(self, mouse_pos: (int, int)):
        self.mouse_pos = mouse_pos