from abc import ABC, abstractmethod
from src.main.model.entity.book import Book


class IBookRepository(ABC):

    @abstractmethod
    def find_books_by_author_fio(self, author_fio: str) -> list[Book]:
        pass

    @abstractmethod
    def find_list_of_books(self, *, offset: int = 0, count: int | None = None) -> list[Book]:
        pass

    @abstractmethod
    def find_books_by_vol_num(self, from_num: int, to_num: int) -> list[Book]:
        pass

    @abstractmethod
    def find_books_by_author_and_publisher(self, author_fio: str, publisher: str) -> list[Book]:
        pass

    @abstractmethod
    def find_book_by_title(self, title: str) -> Book:
        pass

    @abstractmethod
    def find_books_by_circulation_higher(self, circulation: int) -> list[Book]:
        pass

    @abstractmethod
    def find_books_by_circulation_lower(self, circulation: int) -> list[Book]:
        pass

    @abstractmethod
    def find_books_by_total_vol_higher(self, total_vol: int) -> list[Book]:
        pass

    @abstractmethod
    def find_books_by_total_vol_lower(self, total_vol: int) -> list[Book]:
        pass

    @abstractmethod
    def create_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def delete_book(self, book_title: str) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
