from datetime import datetime

class Train:
    def __init__(self, number, first_station, last_station, departure_time, arrival_time):
        self._number_of_train = number
        self._first_station = first_station
        self._last_station = last_station
        self._departure_time = datetime.strptime(departure_time, "%d-%m-%Y %H:%M")
        self._arrival_time = datetime.strptime(arrival_time, "%d-%m-%Y %H:%M")
        self._travel_time = self.calculate_travel_time()

    @property
    def number_of_train(self):
        return self._number_of_train

    @property
    def first_station(self):
        return self._first_station

    @property
    def last_station(self):
        return self._last_station

    @property
    def departure_date(self):
        return self._departure_time.date().strftime("%d-%m-%Y")

    @property
    def departure_time(self):
        return self._departure_time.time().strftime("%H:%M")

    @property
    def arrival_date(self):
        return self._arrival_time.date().strftime("%d-%m-%Y")

    @property
    def arrival_time(self):
        return self._arrival_time.time().strftime("%H:%M")

    @property
    def travel_time(self):
        return self._travel_time

    def __str__(self):
        days, remainder = divmod(self._travel_time.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02} days {:02}:{:02}".format(int(days), int(hours), int(minutes))

    def calculate_travel_time(self):
        travel_time = self._arrival_time - self._departure_time
        return travel_time