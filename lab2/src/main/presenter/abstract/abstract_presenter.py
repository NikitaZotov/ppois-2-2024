from abc import ABC, abstractmethod
from model.repository import IBookRepository
from view.abstract.window import Window


class AbstractPresenter(ABC):
    def __init__(self, window: Window):
        self._window = window
        self._repo: IBookRepository | None = None
        self._do_subscriptions()

    @abstractmethod
    def _do_subscriptions(self) -> None: pass