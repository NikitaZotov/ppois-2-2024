from .db_properties import *
import atexit
import mysql.connector
from src.main.exception.db_exception import DatabaseException


def close_connection() -> None:
    try:
        connection.close()
    except Exception as e:
        raise DatabaseException('Can not create connection', err)


connection = None

try:
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database=DATABASE
    )
except mysql.connector.Error as err:
    raise DatabaseException("Can't create connection", err)

atexit.register(close_connection)