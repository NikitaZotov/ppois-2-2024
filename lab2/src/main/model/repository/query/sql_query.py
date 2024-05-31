import enum
from dataclasses import dataclass


@dataclass
class SqlQuery:

    def __init__(self):
        pass

    FIND_ALL: str = 'SELECT * FROM books'

    FIND_ALL_WITH_PAGES: str = 'SELECT * FROM books LIMIT %s, %s'

    FIND_BY_AUTHOR: str = 'SELECT * FROM books WHERE author_fio = %s'

    FIND_BY_AUTHOR_AND_PUBLISHER: str = 'SELECT * FROM books WHERE author_fio = %s AND publisher = %s'

    FIND_BY_TITLE: str = 'SELECT * FROM books WHERE title = %s'

    FIND_BY_CIRCULATION_HIGHER: str = 'SELECT * FROM books WHERE circulation > %s'

    FIND_BY_CIRCULATION_LOWER: str = 'SELECT * FROM books WHERE circulation < %s'

    FIND_BY_TOTAL_HIGHER: str = 'SELECT * FROM books WHERE books.total_volumes > %s'

    FIND_BY_TOTAL_LOWER: str = 'SELECT * FROM books WHERE books.total_volumes < %s'

    FIND_BY_VOL_NUM_RANGE: str = 'SELECT * FROM books WHERE books.volumes_num >= %s AND books.volumes_num <= %s'

    CREATE_BOOK: str = ('INSERT INTO books (title, author_fio, publisher, volumes_num, circulation, total_volumes) '
                        'VALUES (%s, %s, %s, %s, %s, %s)')

    UPDATE_BOOK: str = ('UPDATE books SET author_fio = %s, publisher = %s,'
                        ' volumes_num = %s, circulation = %s, total_volumes = %s WHERE title = %s')

    DELETE_BOOK: str = 'DELETE FROM books WHERE title = %s'
