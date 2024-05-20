from sqlite3 import connect, Connection

from mailbox import *
from variables import (
    DB_DIR,
    DATABASES,
    receivers_dict
)
from get_data_from_db import (
    get_mail_by_id,
    get_mails_id_by_name,
    get_locker_id,
    get_receivers_notifications_id_by_name
)


def check_mail_existence(mail: Mail) -> bool:
    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM mails''')
    for _, sender, receiver, content in curr.fetchall():
        if sender == str(mail.sender) and receiver == str(mail.receiver) and content == mail.content:
            return True
    return False


def insert_mail(mail: Mail) -> bool:
    if check_mail_existence(mail):
        return False

    conn: Connection = connect(DB_DIR + DATABASES['mails'])
    curr = conn.cursor()
    curr.execute('''INSERT INTO mails (SenderName, ReceiverName, Content)
                    VALUES (?, ?, ?)''',
                 (mail.sender.name, mail.receiver.name, mail.content))
    conn.commit()
    return True


def check_receiver_existence(receiver: Receiver) -> bool:
    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM receivers''')
    for name, _, _ in curr.fetchall():
        if receiver.name == name:
            return True
    return False


def insert_receiver(receiver: Receiver) -> None:
    if check_receiver_existence(receiver):
        return False

    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''INSERT INTO receivers (Name, Mails, Notifications)
                    VALUES (?, ?, ?)''',
                 (receiver.name, -1, -1))
    conn.commit()
    return True


def check_sender_existence(sender: Sender) -> bool:
    conn: Connection = connect(DB_DIR + DATABASES['senders'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM senders''')
    for name, _ in curr.fetchall():
        if sender.name == name:
            return True
    return False


def insert_sender(sender: Sender) -> None:
    if check_sender_existence(sender):
        return False

    conn: Connection = connect(DB_DIR + DATABASES['senders'])
    curr = conn.cursor()
    curr.execute('''INSERT INTO senders (Name, Mails)
                    VALUES (?, ?)''',
                 (sender.name, -1))
    conn.commit()
    return True


def insert_notification(locker_id: int, mail_id: int, password: int) -> None:
    mail: Mail = get_mail_by_id(mail_id)
    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''INSERT INTO notifications (SenderName, ReceiverName, LockerId, Password) VALUES (?, ?, ?, ?)''',
                 (mail.sender.name, mail.receiver.name, locker_id, password))
    conn.commit()
    insert_receiver_notification(locker_id, password)


def insert_mails_in_lockers(sender_name: str) -> None:
    mails_str: str = get_mails_id_by_name(sender_name, True)
    if mails_str == '-1':
        return

    for mail_id in mails_str.split():
        conn: Connection = connect(DB_DIR + DATABASES['lockers'])
        curr = conn.cursor()
        mail_password: int = randint(0, 9999)
        curr.execute('''INSERT INTO lockers (Password, MailId) VALUES (?, ?)''', (mail_password, mail_id))
        conn.commit()
        insert_notification(get_locker_id(mail_password, int(mail_id)), int(mail_id), mail_password)


def insert_receiver_notification(locker_id: int, password: int) -> None:
    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM notifications WHERE LockerId = ? AND Password = ?''', (locker_id, password))
    notification_id, _, receiver, _, _ = curr.fetchall()[0]

    receiver: Receiver = receivers_dict[receiver]
    notifications_str: str = get_receivers_notifications_id_by_name(receiver.name)

    if notifications_str == '-1':
        updated_notifications = str(notification_id)
    else:
        updated_notifications = notifications_str + ' ' + str(notification_id)

    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''UPDATE receivers SET Notifications = ? WHERE Name = ?''',
                 (updated_notifications, receiver.name))
    conn.commit()
