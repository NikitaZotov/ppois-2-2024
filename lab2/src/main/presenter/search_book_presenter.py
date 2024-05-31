import tkinter.messagebox

import utils
from exception import RepositoryException
from model.entity import Book
from model.repository import IBookRepository
from presenter.abstract.abstract_presenter import AbstractPresenter
from view.search_book_window import SearchBookWindow


class SearchBookPresenter(AbstractPresenter):

    def __init__(self, window: SearchBookWindow, repo: IBookRepository):
        super().__init__(window)
        self._repo = repo
        self._window = window
        self._books: list[Book] = []
        self._is_higher_circ = False
        self._is_higher_total = False

    def _do_subscriptions(self) -> None:
        self._window.subscribe("<ok_button_click>", self.__ok_button_click_handler)
        self._window.subscribe("<find_button_click>", self.__search_button_click_handler)
        self._window.subscribe("<higher_checkbutton_click>", self.__higher_checkbutton_click_handler)

    def __ok_button_click_handler(self):
        self._window.destroy()

    def __search_button_click_handler(self):
        match self._window.notebook.tabs().index(self._window.notebook.select()):
            case 0:
                self.__search_by_title()
            case 1:
                self.__search_by_author()
            case 2:
                self.__search_by_author_and_publisher()
            case 3:
                self.__search_by_volumes_number_in_range()
            case 4:
                self.__search_by_circulation()
            case 5:
                self.__search_by_total_vols()

    def __search_by_title(self):
        try:
            self._books = [self._repo.find_book_by_title(self._window.search_args["title"].get())]
        except RepositoryException:
            tkinter.messagebox.showinfo(
                "Message",
                "Nothing was found",
                master=self._window
            )
        utils.clear_tree(self._window.search_tree)
        for book in self._books:
            utils.add_book_to_tree(self._window.search_tree, book)

    def __search_by_author(self):
        try:
            self._books = self._repo.find_books_by_author_fio(self._window.search_args["author_fio"].get())
        except RepositoryException:
            tkinter.messagebox.showinfo(
                "Message",
                "Nothing was found",
                master=self._window
            )
        utils.clear_tree(self._window.search_tree)
        for book in self._books:
            utils.add_book_to_tree(self._window.search_tree, book)

    def __search_by_author_and_publisher(self):
        try:
            self._books = self._repo.find_books_by_author_and_publisher(self._window.search_args["author_fio"].get(),
                                                                        self._window.search_args["publisher"].get())
        except RepositoryException:
            tkinter.messagebox.showinfo(
                "Message",
                "Nothing was found",
                master=self._window
            )
        utils.clear_tree(self._window.search_tree)
        for book in self._books:
            utils.add_book_to_tree(self._window.search_tree, book)

    def __search_by_volumes_number_in_range(self):
        try:
            self._books = self._repo.find_books_by_vol_num(int(self._window.search_args["volumes_from"].get()),
                                                           int(self._window.search_args["volumes_to"].get()))
        except RepositoryException:
            tkinter.messagebox.showinfo(
                "Message",
                "Nothing was found",
                master=self._window
            )
        utils.clear_tree(self._window.search_tree)
        for book in self._books:
            utils.add_book_to_tree(self._window.search_tree, book)

    def __search_by_circulation(self):
        try:
            if self._is_higher_circ:
                self._books = self._repo.find_books_by_circulation_higher(int(self._window.search_args["circulation"]
                                                                              .get()))
            else:
                self._books = self._repo.find_books_by_circulation_lower(int(self._window.search_args["circulation"]
                                                                             .get()))
        except RepositoryException:
            tkinter.messagebox.showinfo(
                "Message",
                "Nothing was found",
                master=self._window
            )
        utils.clear_tree(self._window.search_tree)
        for book in self._books:
            utils.add_book_to_tree(self._window.search_tree, book)

    def __search_by_total_vols(self):
        try:
            if self._is_higher_total:
                self._books = self._repo.find_books_by_total_vol_higher(int(self._window.search_args["total_volumes"]
                                                                            .get()))
            else:
                self._books = self._repo.find_books_by_total_vol_lower(int(self._window.search_args["total_volumes"]
                                                                           .get()))
        except RepositoryException:
            tkinter.messagebox.showinfo(
                "Message",
                "Nothing was found",
                master=self._window
            )
        utils.clear_tree(self._window.search_tree)
        for book in self._books:
            utils.add_book_to_tree(self._window.search_tree, book)

    def __higher_checkbutton_click_handler(self):
        index = self._window.notebook.tabs().index(self._window.notebook.select())
        if index == 4:
            self._is_higher_circ = not self._is_higher_circ
        elif index == 5:
            self._is_higher_total = not self._is_higher_total

