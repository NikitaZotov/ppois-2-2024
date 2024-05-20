from sqlite3 import connect, Connection
import os.path

from variables import (
    DB_DIR,
    DATABASES
)


def create_directory() -> None:
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)


def create_lockers_db() -> None:
    if os.path.exists(DB_DIR + DATABASES['lockers']):
        return

    conn: Connection = connect(DB_DIR + DATABASES['lockers'])
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS lockers (
            id INTEGER PRIMARY KEY,
            Password INTEGER,
            MailId INTEGER)''')
    conn.commit()


def create_mails_db() -> None:
    if os.path.exists(DB_DIR + DATABASES['mails']):
        return

    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS mails (
            id INTEGER PRIMARY KEY,
            SenderName TEXT,
            ReceiverName TEXT,
            Content TEXT)''')
    conn.commit()


def create_notifications_db() -> None:
    if os.path.exists(DB_DIR + DATABASES['notifications']):
        return

    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY,
            SenderName TEXT,
            ReceiverName TEXT,
            LockerId INTEGER,
            Password INTEGER)''')
    conn.commit()


def create_receivers_db() -> None:
    if os.path.exists(DB_DIR + DATABASES['receivers']):
        return

    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS receivers (
            Name TEXT,
            Mails TEXT,
            Notifications TEXT)''')
    conn.commit()


def create_senders_db() -> None:
    if os.path.exists(DB_DIR + DATABASES['senders']):
        return

    conn: Connection = connect(DB_DIR + DATABASES['senders'])
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS senders (
            Name TEXT,
            Mails TEXT)''')
    conn.commit()


def create_tables() -> None:
    create_lockers_db()
    create_mails_db()
    create_notifications_db()
    create_receivers_db()
    create_senders_db()


def main() -> None:
    create_directory()
    create_tables()
