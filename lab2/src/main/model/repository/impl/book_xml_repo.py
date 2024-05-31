import os.path
from xml import sax

from exception import NothingFoundException
from model.entity import Book
from src.main.model.repository import IBookRepository
from xml.etree import ElementTree as ET
from model.repository.xml_handling.sax_handler import SaxHandler


class BookXmlRepo(IBookRepository):

    def __init__(self, file_name: str):
        self._file_name = file_name
        if os.path.exists(file_name):
            self._tree = ET.parse(file_name)
        else:
            self._tree = ET.ElementTree(ET.Element("books"))

    def find_books_by_author_fio(self, author_fio: str) -> list[Book]:
        pass

    def find_list_of_books(self, **kwargs) -> list[Book]:
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, 0)
        parser.setContentHandler(handler_ := SaxHandler())
        parser.parse(self._file_name)
        if books := handler_.books:
            return books
        raise NothingFoundException()

    def find_books_by_author_and_publisher(self, author_fio: str, publisher: str) -> list[Book]:
        pass

    def find_book_by_title(self, title: str) -> Book:
        pass

    def find_books_by_circulation_higher(self, circulation: int) -> list[Book]:
        pass

    def find_books_by_circulation_lower(self, circulation: int) -> list[Book]:
        pass

    def find_books_by_total_vol_higher(self, total_vol: int) -> list[Book]:
        pass

    def find_books_by_total_vol_lower(self, total_vol: int) -> list[Book]:
        pass

    def find_books_by_vol_num(self, from_num: int, to_num: int) -> list[Book]:
        pass

    def create_book(self, valid_book: Book) -> Book:
        book = ET.SubElement(self._tree.getroot(), "book")
        for field in valid_book:
            book.set(field[0], str(field[1]))
        return valid_book

    def update_book(self, book: Book) -> Book:
        pass

    def delete_book(self, book_id: int) -> None:
        pass

    def commit(self) -> None:
        self._tree.write(self._file_name)

    def count(self) -> int:
        pass

