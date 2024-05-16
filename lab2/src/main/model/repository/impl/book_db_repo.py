from src.main.model.repository.book_repository import IBookRepository
from ..query.sql_query import SqlQuery
from ...entity import Book
from src.main.exception import RepositoryException


class BookDbRepo(IBookRepository):

    def __init__(self, connection):
        self._connection = connection

    def commit(self) -> None:
        self._connection.commit()

    def create_book(self, valid_book: Book) -> Book:
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.CREATE_BOOK, (valid_book.title, valid_book.author_fio,
                                                  valid_book.publisher, valid_book.volumes_num,
                                                  valid_book.circulation,
                                                  valid_book.total_volumes))
            return self.find_book_by_title(valid_book.title)
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()

    def update_book(self, valid_book: Book) -> Book:
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.UPDATE_BOOK, (valid_book.author_fio, valid_book.publisher,
                                                  valid_book.volumes_num, valid_book.circulation,
                                                  valid_book.total_volumes, valid_book.title))
            return self.find_book_by_title(valid_book.title)
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()

    def delete_book(self, book_title: str) -> None:
        cursor = None
        book_from_db = self.find_book_by_title(book_title)
        if book_from_db is None:
            raise RepositoryException("Book not found", book_title)
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.DELETE_BOOK, (book_from_db.title,))
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()

    def find_books_by_author_fio(self, author_fio: str) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_AUTHOR, (author_fio,))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found", author_fio)
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_list_of_books(self, *, offset: int = 0, count: int | None = None) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            if count is None:
                cursor.execute(SqlQuery.FIND_ALL)
            else:
                cursor.execute(SqlQuery.FIND_ALL_WITH_PAGES, (offset, count))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as ex:
            raise RepositoryException("Executing query error", ex)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_books_by_author_and_publisher(self, author_fio: str, publisher: str) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_AUTHOR_AND_PUBLISHER, (author_fio, publisher))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_book_by_title(self, title: str) -> Book:
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_TITLE, (title,))
            row = cursor.fetchone()
            if row is not None:
                return Book(*row)
            else:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()

    def find_books_by_circulation_higher(self, circulation: int) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_CIRCULATION_HIGHER, (circulation,))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_books_by_circulation_lower(self, circulation: int) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_CIRCULATION_LOWER, (circulation,))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_books_by_total_vol_higher(self, total_vol: int) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_TOTAL_HIGHER, (total_vol,))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_books_by_total_vol_lower(self, total_vol: int) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_TOTAL_LOWER, (total_vol,))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def find_books_by_vol_num(self, from_num: int, to_num: int) -> list[Book]:
        cursor = None
        result = []
        try:
            cursor = self._connection.cursor()
            cursor.execute(SqlQuery.FIND_BY_VOL_NUM_RANGE, (from_num, to_num))
            rows = cursor.fetchall()
            for row in rows:
                result.append(Book(*row))
            if len(result) == 0:
                raise RepositoryException("Book not found")
        except Exception as e:
            raise RepositoryException("Executing query error", e)
        finally:
            if cursor is not None:
                cursor.close()
        return result

    def count(self) -> int:
        return len(self.find_list_of_books())
