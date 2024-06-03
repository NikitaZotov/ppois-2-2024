from Classes.Model.Train import Train
from datetime import datetime

class ScheduleOfTrains:
    def __init__(self):
        self._list_of_trains = []

    @property
    def list_of_trains(self):
        return self._list_of_trains

    def copy_list_of_trains(self, new_list):
        self._list_of_trains = new_list

    def clear_list(self):
        self._list_of_trains.clear()

    def count_of_records(self):
        return len(self._list_of_trains)

    def addNewTrain(self, number, first_station, last_station, departure_time, arrival_time):
        train = Train(number, first_station, last_station, departure_time, arrival_time)
        self._list_of_trains.append(train)

    def search_by_code_train(self, code):
        found_trains = [train for train in self._list_of_trains if train.number_of_train == code]
        return found_trains

    def search_by_departure_point(self, point):
        found_trains = [train for train in self._list_of_trains if train.first_station == point]
        return found_trains

    def search_by_arrival_point(self, point):
        found_trains = [train for train in self._list_of_trains if train.last_station == point]
        return found_trains

    def search_by_departure_date(self, date):
        found_trains = [train for train in self._list_of_trains if train.departure_date == date]
        return found_trains

    def search_by_departure_time(self, low_limit_time, high_limit_time):
        low_limit_time = datetime.strptime(low_limit_time, "%H:%M").time()
        high_limit_time = datetime.strptime(high_limit_time, "%H:%M").time()
        found_trains = [train for train in self._list_of_trains
                        if datetime.strptime(train.departure_time, "%H:%M").time() >= low_limit_time and
                        datetime.strptime(train.departure_time, "%H:%M").time() <= high_limit_time]
        return found_trains

    def search_by_arrival_time(self, low_limit_time, high_limit_time):
        low_limit_time = datetime.strptime(low_limit_time, "%H:%M").time()
        high_limit_time = datetime.strptime(high_limit_time, "%H:%M").time()
        found_trains = [train for train in self._list_of_trains
                        if datetime.strptime(train.arrival_time, "%H:%M").time() >= low_limit_time and
                        datetime.strptime(train.arrival_time, "%H:%M").time() <= high_limit_time]
        return found_trains

    def search_by_travel_time(self, low_limit_time, high_limit_time, count_of_days_low_limit, count_of_days_high_limit):
        low_limit_time = datetime.strptime(low_limit_time, "%H:%M").time()
        high_limit_time = datetime.strptime(high_limit_time, "%H:%M").time()
        count_of_days_low_limit = int(count_of_days_low_limit)
        count_of_days_high_limit = int(count_of_days_high_limit)

        found_trains = [train for train in self._list_of_trains
                        if (datetime.min + train.travel_time).time() >= low_limit_time and
                        (datetime.min + train.travel_time).time() <= high_limit_time and
                        train.travel_time.days >= count_of_days_low_limit and
                        train.travel_time.days <= count_of_days_high_limit]
        return found_trains
    '''
    def search_by_travel_time(self, low_limit_time, high_limit_time, count_of_days_low_limit, count_of_days_high_limit):
        low_limit_time = datetime.strptime(low_limit_time, "%H:%M").time()
        high_limit_time = datetime.strptime(high_limit_time, "%H:%M").time()
        found_trains = [train for train in self._list_of_trains
                        if (datetime.min + train.travel_time).time() >= low_limit_time and (
                                    datetime.min + train.travel_time).time() <= high_limit_time]
        return found_trains
    '''
    def removeTrain(self, list_of_trains_to_remove):
        filtered_list_of_trains = [train for train in self._list_of_trains if train not in list_of_trains_to_remove]
        self._list_of_trains = filtered_list_of_trains