import re

from model.entity import Book


class BookValidator:

    valid_title_regex = re.compile(r"^([A-Z][a-z]+)( [A-Za-z][a-z]+)*( [1-9]+)?(: [A-Z][a-z]+( [a-z]+)*)?$")
    valid_publisher_regex = re.compile(r"^[A-Z][a-z]*.?( & [A-Z][a-z]*.?)*( inc.| company)*$")
    valid_author_regex = re.compile(r"^[A-Z][a-z]+(-[A-Z][a-z]+)? [A-Z][a-z]+ [A-Z][a-z]+$")

    def validate_book(self, book: Book) -> Book:
        self.validate_title(book.title)
        self.validate_publisher(book.publisher)
        self.validate_author(book.author_fio)
        return book

    def validate_title(self, title: str) -> None:
        if not self.valid_title_regex.match(title):
            raise ValueError("Invalid title")

    def validate_publisher(self, publisher: str) -> None:
        if not self.valid_publisher_regex.match(publisher):
            raise ValueError("Invalid publisher")

    def validate_author(self, author: str) -> None:
        if not self.valid_author_regex.match(author):
            raise ValueError("Invalid author")