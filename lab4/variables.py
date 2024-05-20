from mailbox import (
    Mailbox,
    Sender,
    Receiver
)

DB_DIR: str = 'res/'
DATABASES: dict[str: str] = {'lockers': 'lockers.db',
                             'mails': 'mails.db',
                             'notifications': 'notifications.db',
                             'receivers': 'receivers.db',
                             'senders': 'senders.db'}


NUMBER_OF_LOCKERS: int = 10
local_mailbox: Mailbox = Mailbox(NUMBER_OF_LOCKERS)

bob: Sender = Sender("Bob")
caleb: Sender = Sender("Caleb")
alex: Sender = Sender("Alex")
nova: Sender = Sender("Nova")
vera: Sender = Sender("Vera")
senders_dict: dict[str: Sender] = {"Bob": bob, "Caleb": caleb, "Alex": alex, "Nova": nova, "Vera": vera}

mya: Receiver = Receiver("Mya")
peter: Receiver = Receiver("Peter")
robert: Receiver = Receiver("Robert")
emma: Receiver = Receiver("Emma")
lana: Receiver = Receiver("Lana")
receivers_dict: dict[str: Receiver] = {"Mya": mya, "Peter": peter, "Robert": robert, "Emma": emma, "Lana": lana}
