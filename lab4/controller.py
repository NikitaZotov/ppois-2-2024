from hotel import *
from server import WebServer
from flask import render_template, request, redirect
import pickle


class CLIController:

    def __init__(self, hotel: Hotel):
        self.hotel = hotel

    def perform(self):
        while True:
            print("1 - Add room")
            print("2 - Show available rooms")
            print("3 - Show all rooms")
            print("4 - Add worker")
            print("5 - Show unemployed workers")
            print("6 - Show all workers")
            print("7 - Fire off worker")
            print("8 - Book room")
            print("9 - Pay off for room")
            print("10 - Ask for service")
            print("11 - Ask for restaurant service")
            print("12 - Show uncompleted services: ")
            print("13 - Finish service: ")
            print("14 - Show all visitors: ")
            print("15 - Show all bookings: ")
            choice = input("Choice: ")
            # os.system('cls' if os.name == 'nt' else 'clear')
            if choice == '1':
                room_number = input("Input number of room: ")
                type_of_room = input("Input type of room: ")
                self.hotel.add_room(room_number, type_of_room)
            elif choice == '2':
                self.hotel.show_available_rooms()
            elif choice == '3':
                self.hotel.show_all_rooms()
            elif choice == '4':
                try:
                    name = input("Enter name of worker: ")
                    age = int(input("Enter age of the worker: "))
                    passport_id = input("Enter worker passport id: ")
                    self.hotel.add_worker(name, age, passport_id)
                except ValueError:
                    print("Age must be an integer")
            elif choice == '5':
                self.hotel.show_unemployed_workers()
            elif choice == '6':
                self.hotel.show_all_workers()
            elif choice == '7':
                worker_passport_id = input("Enter worker passport id: ")
                self.hotel.fire_off_worker(worker_passport_id)
            elif choice == '8':
                try:
                    name = input("Enter name of visitor: ")
                    age = int(input("Enter age of the visitor: "))
                    passport_id = input("Enter visitor passport id: ")
                    room_number = input("Enter number of room: ")
                    number_of_days = int(input("Enter for how long (in days): "))
                    self.hotel.book_room(name, age, passport_id, room_number, number_of_days)
                except ValueError:
                    print("Age and number of days must be an integer")
            elif choice == '9':
                visitor_passport_id = input("Input visitor passport id: ")
                self.hotel.pay_off(visitor_passport_id)
            elif choice == '10':
                worker_passport_id = input("Enter worker passport id: ")
                visitor_passport_id = input("Enter visitor passport id: ")
                service_type = input("Enter type of service: ")
                self.hotel.ask_for_service(worker_passport_id, visitor_passport_id, service_type)
            elif choice == '11':
                worker_passport_id = input("Enter worker passport id: ")
                visitor_passport_id = input("Enter visitor passport id: ")
                dishes: list[Dishes] = []
                dish = input("Enter name of dish or stop to end order: ")
                while dish != "stop":
                    try:
                        dishes.append(Dishes[dish])
                        dish = input("Enter name of dish or stop to end order: ")
                    except KeyError:
                        print("No such dish")
                        dish = input("Enter name of dish or stop to end order: ")
                if dishes:
                    self.hotel.ask_for_restaurant_service(worker_passport_id, visitor_passport_id, dishes)
                else:
                    print("You must order something")
            elif choice == '12':
                self.hotel.show_uncompleted_services()
            elif choice == '13':
                worker_passport_id = input("Enter worker passport id: ")
                self.hotel.finish_service(worker_passport_id)
            elif choice == '14':
                self.hotel.show_all_visitors()
            elif choice == '15':
                self.hotel.show_all_bookings()
            else:
                with open('resources/save.pkl', 'wb') as f:
                    pickle.dump(self.hotel, f)
                print("SERVER STOPPED!")
                exit()


class WebController:

    def __init__(self, hotel: Hotel, webserver: WebServer):
        self.hotel = hotel
        self.webserver = webserver
        self.webserver.add_route(route="/", handler_func=WebController.hello_hotel, methods=["GET"])
        self.webserver.add_route(route="/book-available-rooms", handler_func=self.show_available_rooms_and_book_room,
                                 methods=["GET", "POST"])
        self.webserver.add_route(route="/rooms", handler_func=self.add_and_show_rooms,
                                 methods=["GET", "POST"])
        self.webserver.add_route(route="/finish-bookings", handler_func=self.finish_and_show_all_bookings,
                                 methods=["GET", "POST"])
        self.webserver.add_route(route="/workers", handler_func=self.add_and_show_workers,
                                 methods=["GET", "POST"])
        self.webserver.add_route(route="/fire-off-workers", handler_func=self.show_and_fire_off_unemployed_workers,
                                 methods=["GET", "POST"])
        self.webserver.add_route(route="/service-and-visitors", handler_func=self.ask_for_service_and_show_visitors,
                                 methods=["GET", "POST"])
        self.webserver.add_route(route="/finish-service", handler_func=self.finish_service, methods=["POST"])

    def perform(self):
        self.webserver.run()

    @staticmethod
    def hello_hotel():
        return render_template("hotel_root.html")

    def show_available_rooms_and_book_room(self):
        if request.method == "POST":
            name = request.form.get('name')
            age = int(request.form.get('age'))
            passport_id = request.form.get('passport_id')
            room_number = request.form.get('room_number')
            number_of_days = int(request.form.get('number_of_days'))
            book_info = self.hotel.book_room(name, age, passport_id, room_number, number_of_days, show=False)
            if book_info is not None:
                book_info_str = str(book_info)
                book_info_str = book_info_str.replace("\n", "%20")
                book_info_str = book_info_str.replace(" ", "%20")
                return redirect('/book-available-rooms?book_info=' + book_info_str)
            else:
                return redirect('/book-available-rooms')

        book_info_str = request.args.get('book_info', default=None)
        if book_info_str is not None:
            book_info_str.replace("%20", " ")
        available_rooms = self.hotel.show_available_rooms(show=False)
        return render_template('book_available_rooms.html', available_rooms=available_rooms, book_info=book_info_str)

    def add_and_show_rooms(self):
        if request.method == "POST":
            room_number = request.form.get("room_number")
            type_of_room = request.form.get("type_of_room")
            self.hotel.add_room(room_number, type_of_room)
            return redirect('/rooms')

        all_rooms = self.hotel.show_all_rooms(show=False)
        return render_template("add_and_show_rooms.html", all_rooms=all_rooms)

    def finish_and_show_all_bookings(self):
        if request.method == "POST":
            visitor_passport_id = request.form.get("visitor_passport_id")
            payment = self.hotel.pay_off(visitor_passport_id, show=False)
            return redirect('/finish-bookings?payment=' + str(payment))

        payment_info = request.args.get('payment', default=None)
        return render_template("finish_and_show_all_bookings.html",
                               all_bookings=self.hotel.show_all_bookings(show=False), payment_info=payment_info)

    def add_and_show_workers(self):
        if request.method == "POST":
            worker_name = request.form.get("worker_name")
            worker_age = request.form.get("worker_age")
            worker_passport_id = request.form.get("worker_passport_id")
            self.hotel.add_worker(worker_name, int(worker_age), worker_passport_id)
            return redirect("/workers")
        all_workers = self.hotel.show_all_workers(show=False)
        return render_template("add_and_show_workers.html", all_workers=all_workers)

    def show_and_fire_off_unemployed_workers(self):
        if request.method == "POST":
            worker_passport_id = request.form.get("worker_passport_id")
            self.hotel.fire_off_worker(worker_passport_id, show=False)
            return redirect("/fire-off-workers")
        unemployed_workers = self.hotel.show_unemployed_workers(show=False)
        return render_template("fire_off_unemployed_workers.html", unemployed_workers=unemployed_workers)

    def ask_for_service_and_show_visitors(self):
        if request.method == "POST":
            worker_passport_id = request.form.get("worker_passport_id")
            visitor_passport_id = request.form.get("visitor_passport_id")
            service_type = request.form.get("type_of_service")
            self.hotel.ask_for_service(worker_passport_id, visitor_passport_id, service_type, show=False)
        visitors = self.hotel.show_all_visitors(show=False)
        services = self.hotel.show_uncompleted_services(show=False)
        return render_template("services_and_visitors.html", visitors=visitors, services=services)

    def finish_service(self):
        worker_passport_id = request.form.get("worker_passport_id", default="")
        self.hotel.finish_service(worker_passport_id, show=False)
        return redirect("/service-and-visitors")
