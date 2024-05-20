from typing import List

from flask import Flask, render_template, request, url_for, redirect

from mailbox import Mail, Notification
from insert_data_in_db import check_mail_existence
from get_data_from_db import get_all_mails_by_name, get_all_notifications_by_name
from variables import senders_dict, receivers_dict
from insert_data_in_db import insert_sender, insert_receiver
from create_db import main as create_tables
from other_scripts import (
    receiver_get_mail,
    receiver_remove_all_mails,
    sender_sent_all_mails,
    sender_write_mail,
    check_if_mail_is_receivers
)


def insert_start_senders() -> None:
    for sender in senders_dict.values():
        insert_sender(sender)


def insert_start_receivers() -> None:
    for receiver in receivers_dict.values():
        insert_receiver(receiver)


def start() -> None:
    create_tables()
    insert_start_senders()
    insert_start_receivers()


app = Flask(__name__)


@app.route('/')
def menu():
    return render_template("menu.html")


@app.route('/receiver_emma')
def receiver_emma():
    have_mails: bool = False
    have_notifications: bool = False
    mails: List[Mail] = get_all_mails_by_name('Emma', False)
    notifications: List[Notification] = get_all_notifications_by_name('Emma')

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])
    if notifications:
        have_notifications = True
        result_notifications: List[list[str]] = []
        for notification in notifications:
            result_notifications.append([notification.sender, notification.receiver,
                                         notification.locker, notification.password])

    if have_mails and have_notifications:
        return render_template("receiver_emma.html", mails=result_mails, notifications=result_notifications)
    elif have_mails and not have_notifications:
        return render_template("receiver_emma.html", mails=result_mails)
    elif not have_mails and have_notifications:
        return render_template("receiver_emma.html", notifications=result_notifications)
    else:
        return render_template("receiver_emma.html")


@app.route('/receiver_lana')
def receiver_lana():
    have_mails: bool = False
    have_notifications: bool = False
    mails: List[Mail] = get_all_mails_by_name('Lana', False)
    notifications: List[Notification] = get_all_notifications_by_name('Lana')

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])
    if notifications:
        have_notifications = True
        result_notifications: List[list[str]] = []
        for notification in notifications:
            result_notifications.append([notification.sender, notification.receiver,
                                         notification.locker, notification.password])

    if have_mails and have_notifications:
        return render_template("receiver_lana.html", mails=result_mails, notifications=result_notifications)
    elif have_mails and not have_notifications:
        return render_template("receiver_lana.html", mails=result_mails)
    elif not have_mails and have_notifications:
        return render_template("receiver_lana.html", notifications=result_notifications)
    else:
        return render_template("receiver_lana.html")


@app.route('/receiver_mya')
def receiver_mya():
    have_mails: bool = False
    have_notifications: bool = False
    mails: List[Mail] = get_all_mails_by_name('Mya', False)
    notifications: List[Notification] = get_all_notifications_by_name('Mya')

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])
    if notifications:
        have_notifications = True
        result_notifications: List[list[str]] = []
        for notification in notifications:
            result_notifications.append([notification.sender, notification.receiver,
                                         notification.locker, notification.password])

    if have_mails and have_notifications:
        return render_template("receiver_mya.html", mails=result_mails, notifications=result_notifications)
    elif have_mails and not have_notifications:
        return render_template("receiver_mya.html", mails=result_mails)
    elif not have_mails and have_notifications:
        return render_template("receiver_mya.html", notifications=result_notifications)
    else:
        return render_template("receiver_mya.html")


@app.route('/receiver_peter')
def receiver_peter():
    have_mails: bool = False
    have_notifications: bool = False
    mails: List[Mail] = get_all_mails_by_name('Peter', False)
    notifications: List[Notification] = get_all_notifications_by_name('Peter')

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])
    if notifications:
        have_notifications = True
        result_notifications: List[list[str]] = []
        for notification in notifications:
            result_notifications.append([notification.sender, notification.receiver,
                                         notification.locker, notification.password])

    if have_mails and have_notifications:
        return render_template("receiver_peter.html", mails=result_mails, notifications=result_notifications)
    elif have_mails and not have_notifications:
        return render_template("receiver_peter.html", mails=result_mails)
    elif not have_mails and have_notifications:
        return render_template("receiver_peter.html", notifications=result_notifications)
    else:
        return render_template("receiver_peter.html")


@app.route('/receiver_robert')
def receiver_robert():
    have_mails: bool = False
    have_notifications: bool = False
    mails: List[Mail] = get_all_mails_by_name('Robert', False)
    notifications: List[Notification] = get_all_notifications_by_name('Robert')

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])
    if notifications:
        have_notifications = True
        result_notifications: List[list[str]] = []
        for notification in notifications:
            result_notifications.append([notification.sender, notification.receiver,
                                         notification.locker, notification.password])

    if have_mails and have_notifications:
        return render_template("receiver_robert.html", mails=result_mails, notifications=result_notifications)
    elif have_mails and not have_notifications:
        return render_template("receiver_robert.html", mails=result_mails)
    elif not have_mails and have_notifications:
        return render_template("receiver_robert.html", notifications=result_notifications)
    else:
        return render_template("receiver_robert.html")


@app.route('/sender_alex')
def sender_alex():
    have_mails: bool = False
    mails: List[Mail] = get_all_mails_by_name('Alex', True)

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])

    if have_mails:
        return render_template("sender_alex.html", mails=result_mails)
    return render_template("sender_alex.html")


@app.route('/sender_bob')
def sender_bob():
    have_mails: bool = False
    mails: List[Mail] = get_all_mails_by_name('Bob', True)

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])

    if have_mails:
        return render_template("sender_bob.html", mails=result_mails)
    return render_template("sender_bob.html")


@app.route('/sender_caleb')
def sender_caleb():
    have_mails: bool = False
    mails: List[Mail] = get_all_mails_by_name('Caleb', True)

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])

    if have_mails:
        return render_template("sender_caleb.html", mails=result_mails)
    return render_template("sender_caleb.html")


@app.route('/sender_nova')
def sender_nova():
    have_mails: bool = False
    mails: List[Mail] = get_all_mails_by_name('Nova', True)

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])

    if have_mails:
        return render_template("sender_nova.html", mails=result_mails)
    return render_template("sender_nova.html")


@app.route('/sender_vera')
def sender_vera():
    have_mails: bool = False
    mails: List[Mail] = get_all_mails_by_name('Vera', True)

    if mails:
        have_mails = True
        result_mails: List[list[str]] = []
        for mail in mails:
            result_mails.append([mail.sender, mail.receiver, mail.content])

    if have_mails:
        return render_template("sender_vera.html", mails=result_mails)
    return render_template("sender_vera.html")


@app.route('/write_mail_menu', methods=['GET', 'POST'])
def write_mail_menu():
    if request.method == 'POST':
        sender = request.form.get('senders')
        receiver = request.form.get('receivers')
        content = request.form.get('content')

        if not sender or not receiver or not content:
            error_message = "Please select options from both sets and enter some text before submitting."
            return render_template("write_mail_menu.html", error=error_message)

        if check_mail_existence(Mail(sender, receiver, content)):
            error_message = "This mail already exists."
            return render_template("write_mail_menu.html", error=error_message)

        sender_write_mail(sender, receiver, content)
    return render_template("write_mail_menu.html")


@app.route('/get_mail_menu', methods=['GET', 'POST'])
def get_mail_menu():
    if request.method == 'POST':
        receiver = request.form.get('receivers')
        locker = request.form.get('locker')
        password = request.form.get('password')

        if not receiver or not locker or not password:
            error_message = "Please select options from both sets and enter some text before submitting."
            return render_template("get_mail_menu.html", error=error_message)

        if not check_if_mail_is_receivers(int(locker), receiver):
            error_message = "This is not my locker."
            return render_template("get_mail_menu.html", error=error_message)
        else:
            if not receiver_get_mail(receiver, int(locker), int(password)):
                error_message = "This password is incorrect."
                return render_template("get_mail_menu.html", error=error_message)
            else:
                m = f"{receiver} got a mail."
                return render_template("get_mail_menu.html", message=m)

    return render_template("get_mail_menu.html")


@app.route('/refresh', methods=['POST'])
def refresh():
    return_url = request.form.get('return_url')
    if 'sender' in return_url:
        sender_sent_all_mails(return_url[8:].title())
    if 'receiver' in return_url:
        receiver_remove_all_mails(return_url[10:].title())

    if not return_url:
        return_url = url_for('menu')
    return redirect(return_url)

@app.route('/check_mailbox_condition')
def check_mailbox_condition():
    return render_template("check_mailbox_condition.html")


if __name__ == "__main__":
    start()
    app.run(debug=True)
