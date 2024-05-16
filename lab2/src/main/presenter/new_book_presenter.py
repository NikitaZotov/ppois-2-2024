import tkinter.messagebox

from model.entity import Book
from presenter.abstract.abstract_presenter import AbstractPresenter
from presenter.validator import BookValidator
from view.new_book_window import NewBookWindow


class NewBookPresenter(AbstractPresenter):

    def __init__(self, window: NewBookWindow, *, validator=BookValidator()):
        super().__init__(window)
        self._new_book: Book | None = None
        self._validator = validator

    def _do_subscriptions(self) -> None:
        self._window.subscribe("<ok_button_click>", self.__ok_button_click_handler)

    @property
    def new_book(self) -> Book | None:
        return self._new_book

    def __ok_button_click_handler(self, **kwargs) -> None:
        try:
            self._new_book = self._validator.validate_book(Book(*kwargs.values()))
            self._window.destroy()
        except ValueError as err:
            tkinter.messagebox.showerror("Error", str(err), master=self._window)
