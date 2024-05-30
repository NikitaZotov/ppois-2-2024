from .event import Event


class InputEvent(Event):
    name = "Input event"

    def __init__(self, unicode_char, click_pos: (int, int)):
        self.char = unicode_char
        self.click_pos = click_pos

    def __str__(self):
        return '%s, char=%s, click_pos=%s' % (self.name, self.char, self.click_pos)
