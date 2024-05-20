from sqlite3 import connect, Connection

from create_db import (
    DB_DIR,
    DATABASES
)
from variables import (
    senders_dict,
    receivers_dict
)
from mailbox import *


def get_locker_id(password: int, mail_id: int) -> int:
    conn: Connection = connect(DB_DIR + DATABASES['lockers'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM lockers WHERE PASSWORD = ? AND MailId = ?''', (password, mail_id))
    return curr.fetchone()[0]


def get_mail_id(mail: Mail) -> int:
    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM mails WHERE SenderName = ? AND ReceiverName = ? AND Content = ?''',
                 (mail.sender.name, mail.receiver.name, mail.content))
    return curr.fetchone()[0]


def get_mail_by_id(mail_id: int) -> Mail:
    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM mails WHERE id = ?''', (mail_id,))
    _, sender, receiver, content = curr.fetchone()
    return Mail(senders_dict[sender], receivers_dict[receiver], content)


def get_mails_id_by_name(name: str, is_sender: bool) -> str:
    conn: Connection = connect(DB_DIR + DATABASES['senders' if is_sender else 'receivers'])
    curr = conn.cursor()
    if is_sender:
        curr.execute('''SELECT * FROM senders WHERE NAME = ?''', (name,))
    else:
        curr.execute('''SELECT * FROM receivers WHERE NAME = ?''', (name,))
    return curr.fetchone()[1]


def get_receivers_notifications_id_by_name(name: str) -> str:
    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM receivers WHERE NAME = ?''', (name,))
    notifications_str: str = curr.fetchone()[2]
    conn.commit()
    return notifications_str


def get_notification_id_by_locker_id_and_password(locker_id: int, password: int) -> int:
    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM notifications WHERE LockerId = ? AND Password = ?''', (locker_id, password))
    temp = curr.fetchone()
    if temp is None:
        return -1
    notification_id: int = temp[0]
    conn.commit()
    return notification_id


def get_mail_id_from_locker_by_locker_id_and_password(locker_id: int, password: int) -> int:
    conn: Connection = connect(DB_DIR + DATABASES['lockers'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM lockers WHERE id = ? AND Password = ?''', (locker_id, password))
    temp = curr.fetchone()
    if temp is None:
        return -1
    mail_id = temp[0]
    conn.commit()
    return mail_id


def get_all_mails_by_name(name: str, is_sender: bool) -> List[Mail] | None:
    mails_str: str = get_mails_id_by_name(name, is_sender)
    if mails_str == '-1':
        return
    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute(f'''SELECT * FROM mails WHERE {'SenderName' if is_sender else 'ReceiverName'} = ?''', (name,))
    rows = curr.fetchall()
    mails: List[Mail] = []
    for row in rows:
        if str(row[0]) in mails_str:
            mail: Mail = Mail(*row[1:])
            mails.append(mail)
    return mails


def get_notifications_id_by_name(name: str) -> str:
    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM receivers WHERE Name =?''', (name,))
    return curr.fetchone()[2]


def get_all_notifications_by_name(name: str) -> List[Notification] | None:
    notifications_str: str = get_notifications_id_by_name(name)
    if notifications_str == '-1':
        return

    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM notifications WHERE ReceiverName =?''', (name,))
    rows = curr.fetchall()
    notifications: List[Notification] = []
    for row in rows:
        if str(row[0]) in notifications_str:
            notification: Notification = Notification(*row[1:])
            notifications.append(notification)
    return notifications
