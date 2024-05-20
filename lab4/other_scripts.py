from sqlite3 import connect, Connection

from mailbox import *
from create_db import (
    DB_DIR,
    DATABASES
)
from remove_data_from_db import (
    remove_lockers_by_locker_id_password,
    remove_notification_by_locker_id_password,
    remove_mail_by_id
)
from variables import (
    senders_dict,
    receivers_dict
)
from insert_data_in_db import (
    insert_mail,
    insert_mails_in_lockers
)
from get_data_from_db import (
    get_mail_id,
    get_mails_id_by_name,
    get_receivers_notifications_id_by_name,
    get_notification_id_by_locker_id_and_password,
    get_mail_id_from_locker_by_locker_id_and_password,
)


def sender_write_mail(sender_name: str, receiver_name: str, content: str) -> None:
    sender: Sender = senders_dict[sender_name]
    receiver: Receiver = receivers_dict[receiver_name]
    mail: Mail = Mail(sender, receiver, content)

    if insert_mail(mail):
        mail_id: int = get_mail_id(mail)
        mails_str: str = get_mails_id_by_name(sender_name, True)

        if mails_str == '-1':
            updated_mails = str(mail_id)
        else:
            updated_mails = mails_str + ' ' + str(mail_id)

        conn: Connection = connect(DB_DIR + DATABASES['senders'])
        curr = conn.cursor()
        curr.execute('''UPDATE senders SET Mails = ? WHERE Name = ?''',
                     (updated_mails, sender_name))
        conn.commit()


def sender_sent_all_mails(sender_name: str) -> None:
    insert_mails_in_lockers(sender_name)

    conn: Connection = connect(DB_DIR + DATABASES['senders'])
    curr = conn.cursor()
    curr.execute('''UPDATE senders SET Mails = ? WHERE Name = ?''', ('-1', sender_name))
    conn.commit()


def check_if_mail_is_receivers(locker_id: int, receiver_name: str) -> bool:
    conn: Connection = connect(DB_DIR + DATABASES['notifications'])
    curr = conn.cursor()
    curr.execute('''SELECT * FROM notifications WHERE LockerId = ? AND ReceiverName = ?''', (locker_id, receiver_name))
    for _, _, receiver, locker, _ in curr.fetchall():
        if receiver == receiver_name and locker == locker_id:
            return True
    return False


def receiver_get_mail(receiver_name: str, locker_id: int, password: int) -> bool:
    notifications_str: str = get_receivers_notifications_id_by_name(receiver_name)
    mails_str: str = get_mails_id_by_name(receiver_name, False)
    if notifications_str == '-1':
        return False
    if not check_if_mail_is_receivers(locker_id, receiver_name):
        return False
    mail_id: int = get_mail_id_from_locker_by_locker_id_and_password(locker_id, password)
    if mail_id == -1:
        return False
    notification_id: int = get_notification_id_by_locker_id_and_password(locker_id, password)
    if notification_id == -1:
        return False

    remove_lockers_by_locker_id_password(locker_id, password)
    remove_notification_by_locker_id_password(locker_id, password)

    if mails_str == '-1':
        updated_mails = str(mail_id)
    else:
        updated_mails = mails_str + ' ' + str(mail_id)

    if len(notifications := notifications_str.split()) == 1:
        updated_notifications = '-1'
    else:
        notifications.remove(str(notification_id))
        updated_notifications = ' '.join(notifications)

    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''UPDATE receivers SET Mails = ?, Notifications = ? WHERE Name = ?''',
                 (updated_mails, updated_notifications, receiver_name))
    conn.commit()
    return True


def receiver_remove_all_mails(receiver_name: str) -> None:
    mails_str: str = get_mails_id_by_name(receiver_name, False)
    if mails_str == '-1' or mails_str is None:
        return

    mails_id: list = mails_str.split()
    for mail_id in mails_id:
        remove_mail_by_id(int(mail_id))

    conn: Connection = connect(DB_DIR + DATABASES['receivers'])
    curr = conn.cursor()
    curr.execute('''UPDATE receivers SET mails = ? WHERE Name = ?''', ('-1', receiver_name))
    conn.commit()

