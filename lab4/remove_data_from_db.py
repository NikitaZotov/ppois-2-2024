from sqlite3 import connect, Connection
from variables import DB_DIR, DATABASES


def remove_notification_by_locker_id_password(locker_id: int, password: int) -> None:
    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''DELETE FROM notifications WHERE LockerId = ? AND Password = ?''', (locker_id, password))
    conn.commit()


def remove_lockers_by_locker_id_password(locker_id: int, password: int) -> None:
    conn: Connection = connect(DB_DIR + DATABASES['lockers'])
    curr = conn.cursor()
    curr.execute('''DELETE FROM lockers WHERE id = ? AND Password = ?''', (locker_id, password))
    conn.commit()


def remove_mail_by_id(mail_id: int) -> None:
    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute('''DELETE FROM mails WHERE id = ?''', (mail_id, ))
    conn.commit()
