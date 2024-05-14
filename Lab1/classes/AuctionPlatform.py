from .Lot import Lot
from .Participant import Participant
from .Timer import Timer

class AuctionPlatform:

    def __init__(self):
        self.__lots = []
        self.__participants = []
        self.__timer = Timer(300)

    @property
    def time(self):
        return self.__timer.duration

    @property
    def list_of_participants(self):
        return self.__participants

    def count_lots(self):
        return len(self.__lots)

    def count_participants(self):
        return len(self.__participants)

    def add_lot(self, name, price, bid):
        new_lot = Lot(name, price, bid)
        self.__lots.append(new_lot)

    def add_participant(self, name, money):
        new_participant = Participant(str(self.count_participants() + 1), name, money)
        self.__participants.append(new_participant)

    def install_timer(self, duration):
        self.__timer.reset()
        self.__timer.duration = duration

    def return_lot(self, index):
        return self.__lots[index]

    def return_participant(self, index):
        return self.__participants[index]

