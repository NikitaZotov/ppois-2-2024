from weakref import WeakKeyDictionary
from typing import Callable

from event import Event, TickEvent, HoverEvent, DeletingEvent, EatenEvent
from singleton import singleton


@singleton
class EventManager:
    def __init__(self):
        self.handlers: WeakKeyDictionary[type, list[Callable[[Event], None]]] = WeakKeyDictionary()

    def add_handler(self, event_type: type, handler: Callable[[Event], None]):
        self.handlers.setdefault(event_type, []).append(handler)

    def remove_handler(self, *handlers):
        for handlers_list in self.handlers.values():
            for handler in handlers:
                if handler in handlers_list:
                    handlers_list.remove(handler)
        
    def notify(self, event: Event):
        if (event_type := type(event)) not in self.handlers:
            return

        for handler in self.handlers[event_type]:
            handler(event)


ev_manager = EventManager()
