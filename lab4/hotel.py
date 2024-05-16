from accessify import private
from exceptions import BookingException, VisitorNotFoundException
from reception import Reception
from entities import HotelRoom, Visitor, Booking, Service, Worker
from enums import RoomStatus, RoomType, WorkerStatus, ServiceType, Dishes
from datetime import datetime, timedelta


class Hotel:

    __PAYMENT_PER_DAY = 100

    def __init__(self):
        self.__reception = Reception()
        self.__workers: list[Worker] = []

    def add_worker(self, name: str, age: int, passport_id: str) -> bool:
        for worker in self.__workers:
            if worker.passport_id == passport_id:
                return False
        worker = Worker(name, age, passport_id, WorkerStatus.resting)
        self.__workers.append(worker)
        return True

    def fire_off_worker(self, worker_passport_id: str, show=True) -> bool:
        for worker in self.__workers:
            if worker_passport_id == worker.passport_id and worker.status is WorkerStatus.resting:
                self.__workers.remove(worker)
                return True
        if show:
            print(f"Worker with passport id: {worker_passport_id} is busy or doesn't exist ")
        return False

    def show_unemployed_workers(self, show=True):
        unemployed_workers: list[Worker] = []
        for worker in self.__workers:
            if worker.status == WorkerStatus.resting:
                unemployed_workers.append(worker)
                if show:
                    print(worker)
        return unemployed_workers

    def show_all_workers(self, show=True):
        if show:
            for worker in self.__workers:
                print(worker)
        return self.__workers

    def add_room(self, room_number: str, type_of_room: str) -> bool:
        try:
            type_of_room = RoomType[type_of_room]
            room = HotelRoom(room_number, type_of_room, RoomStatus.empty)
            return self.__reception.add_room(room)
        except KeyError:
            print("No such type of room")
            return False

    def show_available_rooms(self, show=True) -> list[HotelRoom]:
        rooms: list[HotelRoom] = self.__reception.find_available_rooms()
        if show:
            print("Available rooms: ")
            for room in rooms:
                print(room, "\n")

        return rooms

    def show_all_rooms(self, show=True) -> list[HotelRoom]:
        if show:
            for room in self.__reception.rooms:
                print(room, "\n")

        return self.__reception.rooms

    def book_room(self, name: str, age: int, passport_id: str, room_number: str, number_of_days: int, show=True) -> Booking:
        visitor: Visitor = self.registrate_visitor(name, age, passport_id)
        start_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        finish_date = start_date + timedelta(days=number_of_days)
        finish_date = finish_date.replace(hour=12, minute=0, second=0, microsecond=0)
        try:
            book: Booking = self.__reception.book(visitor.passport_id, room_number, start_date, finish_date)
            if show:
                print(book)
            return book
        except BookingException as e:
            if show:
                print(e)
            return None
        except VisitorNotFoundException as e:
            if show:
                print(e)
            return None

    def pay_off(self, visitor_passport_id: str, show=True) -> int:
        try:
            booking: Booking = self.__reception.finish_booking(visitor_passport_id)
            days: int = (booking.finish_date - booking.start_date).days
            if show:
                print(f"""Payment for {days} days is {days * Hotel.__PAYMENT_PER_DAY * booking.room.type.value[1]}""")
            return days * Hotel.__PAYMENT_PER_DAY * booking.room.type.value[1]
        except BookingException as e:
            print(e)
            return 0
        except VisitorNotFoundException as e:
            print(e)
            return 0

    def show_uncompleted_services(self, show=True):
        services: list[Service] = self.__reception.services
        if show:
            for service in services:
                print(service)
        return services

    def ask_for_service(self, worker_passport_id: str, visitor_passport_id: str, service_type: str, show=True) -> bool:
        if service_type == 'restaurant':
            if show:
                print("You should ask for a restaurant service")
            return False
        try:
            for worker in self.__workers:
                if worker.passport_id == worker_passport_id and worker.status is WorkerStatus.resting:
                    type_of_service: ServiceType = ServiceType[service_type]
                    self.__reception.ask_for_service(visitor_passport_id, type_of_service, worker)
                    return True
            if show:
                print(f"Worker with passport id '{worker_passport_id}' is busy or doesn't exist")
            return False
        except KeyError:
            if show:
                print("Invalid type of service")
        except VisitorNotFoundException as e:
            if show:
                print(e)
            return False

    def ask_for_restaurant_service(self, worker_passport_id: str,
                                   visitor_passport_id: str, dishes: list[Dishes]) -> bool:
        try:
            for worker in self.__workers:
                if worker.passport_id == worker_passport_id and worker.status is WorkerStatus.resting:
                    self.__reception.ask_for_restaurant_service(visitor_passport_id, worker, dishes)
                    return True
            print(f"Worker with passport id '{worker_passport_id}' is busy or doesn't exist")
            return False
        except VisitorNotFoundException as e:
            print(e)
            return False

    def finish_service(self, worker_passport_id: str, show=True) -> bool:
        service = self.__reception.finish_service(worker_passport_id)
        if service:
            service.worker.status = WorkerStatus.resting
            if show:
                print("Finished service: ", service, sep="\n")
            return True
        else:
            if show:
                print("No service found")
            return False

    def show_all_visitors(self, show=True):
        if show:
            for visitor in self.__reception.visitors:
                print(visitor, "\n")

        return self.__reception.visitors

    def show_all_bookings(self, show=True):
        if show:
            for booking in self.__reception.bookings:
                print(booking, "\n")

        return self.__reception.bookings

    @private
    def registrate_visitor(self, name: str, age: int, passport_id: str) -> Visitor:
        visitor = Visitor(name, age, passport_id)
        if not self.__reception.registrate_visitor(visitor):
            self.__reception.find_visitor(visitor.passport_id)
        return visitor
