from typing import List
from station import Station
from train import Train
from datetime import timedelta
from depot import Depot


class Schedule:
    def __init__(self):
        self.__stations: List[Station] = []
        self.__trains: List[Train] = []
        self.__depots: List[Depot] = []
        self.__start_time: timedelta = timedelta(hours=5, minutes=30)
        self.__end_time: timedelta = timedelta(hours=00, minutes=40)
        self.__delta_time: timedelta = timedelta(minutes=0)
        self.__trains_counter: int = 0

    def get_stations_list(self):
        return self.__stations

    def add_depot(self, depot: Depot):
        try:
            if len(self.__depots) < 2:
                self.__depots.append(depot)
            else:
                raise ValueError("Метро переполнено депо")
        except ValueError as e:
            print(e)

    def add_train(self, train: Train):
        try:
            if 2 * len(self.__stations) > len(self.__trains):
                self.__trains.append(train)
            else:
                raise ValueError("Метро переполнено поездами!")
        except ValueError as e:
            print(e)

    def fill_depots(self):
        flag: bool = False
        for train in self.__trains[:]:
            if flag is False:
                self.__depots[0].pull_into(train)
                flag = True
            else:
                self.__depots[1].pull_into(train)
                flag = False

    def remove_train(self, train: Train):
        self.__trains.remove(train)

    def add_station(self, station: Station):
        self.__stations.append(station)

    def add_stations(self, stations: List[Station]):
        self.__stations.extend(stations)

    def remove_station(self, station: Station):
        self.__stations.remove(station)

    def set_time_delay(self):
        if timedelta(hours=5, minutes=30) <= self.__start_time <= timedelta(hours=7):
            self.__delta_time = timedelta(minutes=7)
            return
        if timedelta(hours=7) <= self.__start_time <= timedelta(hours=9):
            self.__delta_time = timedelta(minutes=2)
            return
        if timedelta(hours=9) <= self.__start_time <= timedelta(hours=16):
            self.__delta_time = timedelta(minutes=5)
            return
        if timedelta(hours=16) <= self.__start_time <= timedelta(hours=19):
            self.__delta_time = timedelta(minutes=3)
            return
        if timedelta(hours=19) <= self.__start_time <= timedelta(hours=21):
            self.__delta_time = timedelta(minutes=5)
            return
        if timedelta(hours=21) <= self.__start_time <= self.__end_time:
            self.__delta_time = timedelta(minutes=11)
            return

    def print_info(self):
        print(f"It is {self.__start_time}\nNearest train will be in {self.__delta_time}")

    def run_a_train(self):
        try:
            if len(self.__depots[0].get_trains_list()) == 0 and len(self.__depots[1].get_trains_list()) == 0:
                raise ValueError("Depots are empty")
            if self.__stations[0].get_platforms()[0].train is None:
                self.__stations[0].get_platforms()[0].train = self.__depots[0].pull_out_train()
                self.__stations[0].get_platforms()[0].train.platform = self.__stations[0].get_platforms()[0]

                self.__trains_counter += 1
            elif self.__stations[0].get_platforms()[0].train is not None:
                raise ValueError(f"Station {self.__stations[0].number}\n Платформа 0 \nуже имеет поезд")
            if self.__stations[-1].get_platforms()[1].train is None:
                self.__stations[-1].get_platforms()[1].train = self.__depots[1].pull_out_train()
                self.__stations[-1].get_platforms()[1].train.platform = self.__stations[-1].get_platforms()[1]
                self.__trains_counter += 1
            elif self.__stations[-1].get_platforms()[1].train is not None:
                raise ValueError(f"Station {self.__stations[1].number}\n Платформа 1 \nуже имеет поезд")
        except ValueError as e:
            print(e)

    def next_phase(self):
        skip_bool: bool = False
        self.set_time_delay()
        for i in range(len(self.__stations) - 1):

            if self.__stations[len(self.__stations) - 1].get_platforms()[0].train is not None:
                for passenger in self.__stations[len(self.__stations) - 1].get_platforms()[0].train.get_passengers():
                    passenger.disembark(self.__stations[len(self.__stations) - 1].get_platforms()[0].train)
                self.__depots[1].pull_into(self.__stations[len(self.__stations) - 1].get_platforms()[0].train)
                self.__stations[len(self.__stations) - 1].get_platforms()[0].train.platform = None
                self.__stations[len(self.__stations) - 1].get_platforms()[0].train = None
                self.__trains_counter -= 1
            if skip_bool:
                skip_bool = False
                continue
            if self.__stations[i + 1].get_platforms()[0].train is None and self.__stations[i].get_platforms()[0].train is not None :
                skip_bool = True
                self.__stations[i].get_platforms()[0].train.switch_station(self.__stations[i + 1].get_platforms()[0])
                self.__stations[i].get_platforms()[0].train = None
                continue
            elif self.__stations[i + 1].get_platforms()[0].train is not None:
                continue
        skip_bool: bool = False
        for i in range(len(self.__stations) - 1, 0, -1):
            if self.__stations[0].get_platforms()[1].train is not None:
                for passenger in self.__stations[0].get_platforms()[1].train.get_passengers():
                    passenger.disembark(self.__stations[0].get_platforms()[1].train)
                self.__depots[0].pull_into(self.__stations[0].get_platforms()[1].train)
                self.__stations[0].get_platforms()[1].train.platform = None
                self.__stations[0].get_platforms()[1].train = None
                self.__trains_counter -= 1
            if skip_bool:
                skip_bool = False
                continue
            if self.__stations[i - 1].get_platforms()[1].train is None and self.__stations[i].get_platforms()[1].train is not None:
                skip_bool = True
                self.__stations[i].get_platforms()[1].train.switch_station(self.__stations[i-1].get_platforms()[1])
                self.__stations[i].get_platforms()[1].train = None
                continue
            elif self.__stations[i - 1].get_platforms()[1].train is not None:
                continue
        self.__start_time += self.__delta_time
