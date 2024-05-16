import tkinter
import tkinter.messagebox
from exception import NothingFoundException, RepositoryException
from model.db_connection import connection
from model.repository import BookDbRepo
from presenter.abstract.abstract_presenter import AbstractPresenter
import utils
from view.main_window import MainWindow


class MainPresenter(AbstractPresenter):

    def __init__(self, window: MainWindow):
        super().__init__(window)
        self._repo = BookDbRepo(connection)
        self._window = window
        self._books = self._repo.find_list_of_books()
        self._page_size = self._window.indexes["page size"]
        self._total_records = self._window.indexes["total records"]
        self._selected_page = self._window.indexes["current page"]
        self._total_pages = self._window.indexes["total pages"]
        self._tree_view = self._window.tree_view_enabled
        self._page_size.set(10)
        self._selected_page.set(1)
        self.__load_page()

    def _do_subscriptions(self) -> None:
        self._window.subscribe("<add_book_menu_click>", self.__add_book_menu_click_handler)
        self._window.subscribe("<first_page_button_click>", self.__first_page_button_click_handler)
        self._window.subscribe("<last_page_button_click>", self.__last_page_button_click_handler)
        self._window.subscribe("<prev_page_button_click>", self.__prev_page_button_click_handler)
        self._window.subscribe("<next_page_button_click>", self.__next_page_button_click_handler)
        self._window.subscribe("<inc_pages_button_click>", self.__inc_pages_button_click_handler)
        self._window.subscribe("<dec_pages_button_click>", self.__dec_pages_button_click_handler)
        self._window.subscribe("<tree_view_checkbutton_click>", self.__tree_view_checkbutton_click_handler)
        self._window.subscribe("<commit_button_click>", self.__commit_button_click_handler)
        self._window.subscribe("<xml_save_menu_click>", self.__xml_save_menu_click_handler)
        self._window.subscribe("<xml_load_menu_click>", self.__xml_load_menu_click_handler)
        self._window.subscribe("<search_book_menu_click>", self.__search_book_menu_click_handler)
        self._window.subscribe("<delete_book_menu_click>", self.__delete_book_menu_click_handler)

    def __reload_books_tree(self, tree):
        utils.clear_tree(tree)
        for book in self._books:
            utils.add_book_to_tree(tree, book)

    def __load_page(self, page: int = 1) -> None:
        if page < 1:
            raise NothingFoundException
        try:
            page_size = self._page_size.get()
            count = self._repo.count()
            self._total_records.set(count)
            self._total_pages.set(count // page_size + (1 if count % page_size != 0 else 0))
            self._books = self._repo.find_list_of_books(
                offset=page_size * (page - 1),
                count=page_size
            )
        except Exception as e:
            raise e
        self.__reload_books_tree(self._window.book_tree)

    def __change_page(self, page: int):
        try:
            self.__load_page(page)
        except Exception as e:
            raise e
        self._selected_page.set(page)

    def __add_book_menu_click_handler(self):
        utils.create_new_book_subwindow(self._window, self._repo)
        self.__load_page()

    def __first_page_button_click_handler(self):
        self.__change_page(1)

    def __last_page_button_click_handler(self):
        self.__change_page(self._total_pages.get())

    def __prev_page_button_click_handler(self):
        try:
            self.__change_page(self._selected_page.get() - 1)
        except NothingFoundException:
            tkinter.messagebox.showerror("Error", "This page is first.")

    def __next_page_button_click_handler(self):
        try:
            self.__change_page(self._selected_page.get() + 1)
        except NothingFoundException:
            tkinter.messagebox.showerror("Error", "This page is last.")

    def __inc_pages_button_click_handler(self):
        self._page_size.set(self._page_size.get() + 1)
        self.__load_page()

    def __dec_pages_button_click_handler(self):
        if (page_size := self._page_size.get()) < 2:
            tkinter.messagebox.showerror(
                "Error",
                "Page size can't be less then 1",
                master=self._window
            )
            return
        self._page_size.set(self._page_size.get() - 1)
        self.__load_page()

    def __tree_view_checkbutton_click_handler(self):
        if self._tree_view.get():
            self._window.book_tree["displaycolumns"] = ()
            self._window.book_tree["show"] = "tree"
        else:
            self._window.book_tree["displaycolumns"] = tuple(self._window.books_tree_columns.keys())
            self._window.book_tree["show"] = "headings"

    def __commit_button_click_handler(self):
        self._repo.commit()

    def __xml_save_menu_click_handler(self):
        utils.save_to_xml_subwindow(self._books)

    def __xml_load_menu_click_handler(self):
        try:
            for book in utils.load_from_xml_subwindow():
                self.__add_book(book)
                self._repo.create_book(book)
        except NothingFoundException:
            tkinter.messagebox.showerror("", "Nothing was found.")
        except RepositoryException as e:
            tkinter.messagebox.showerror("", str(e))

    def __add_book(self, book):
        self._books.append(book)
        utils.add_book_to_tree(self._window.book_tree, book)

    def __search_book_menu_click_handler(self):
        utils.search_book_subwindow(self._window, self._repo)

    def __delete_book_menu_click_handler(self):
        utils.delete_book_subwindow(self._window, self._repo)
        self.__load_page()


if __name__ == "__main__":
    window = MainWindow()
    presenter = MainPresenter(window)
    window.mainloop()




