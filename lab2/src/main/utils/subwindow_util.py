import tkinter.filedialog
from tkinter.messagebox import showinfo
from model.entity import Book
from model.repository import IBookRepository
from model.repository.impl.book_xml_repo import BookXmlRepo
from presenter.delete_book_presenter import DeleteBookPresenter
from presenter.new_book_presenter import NewBookPresenter
from presenter.search_book_presenter import SearchBookPresenter
from view.abstract.window import Window
from view.delete_book_window import DeleteBookWindow
from view.new_book_window import NewBookWindow
from view.search_book_window import SearchBookWindow


def create_new_book_subwindow(main_window: Window, repo: IBookRepository):
    window = NewBookWindow(main_window)
    presenter = NewBookPresenter(window)
    window.wait_window()
    if book := presenter.new_book:
        try:
            book.total_volumes = int(book.circulation) * int(book.volumes_num)
            repo.create_book(book)
        except Exception as e:
            showinfo("info", "Nothing are found")


def save_to_xml_subwindow(books: list[Book]):
    file = tkinter.filedialog.asksaveasfilename(filetypes=(("XML file", "*.xml"),))
    repo = BookXmlRepo(file)
    for book in books:
        repo.create_book(book)
    repo.commit()


def load_from_xml_subwindow() -> list[Book]:
    file = tkinter.filedialog.askopenfilename(filetypes=(("XML file", "*.xml"),))
    repo = BookXmlRepo(file)
    return repo.find_list_of_books()


def search_book_subwindow(master: Window, repo: IBookRepository) -> None:
    window = SearchBookWindow(master)
    presenter = SearchBookPresenter(window, repo)
    window.wait_window()


def delete_book_subwindow(master: Window, repo: IBookRepository) -> None:
    window = DeleteBookWindow(master)
    presenter = DeleteBookPresenter(window, repo)
    window.wait_window()
