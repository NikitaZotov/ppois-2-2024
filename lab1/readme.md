Лабораторная работа 1, вариант 46
Предметная область: Самолет
![image](https://github.com/NikitaZotov/ppois-2-2024/assets/100913385/c91bdc0a-2493-4266-a351-3668c9658ad1)

В коде были соблюдены такие принципы Solid как Single responsibiliry, open-closed, из принципов ооп - абстракция, полиморфизм

Реализация классов:

основной класс - airplane.py:
from typing import List
from classes.ticket import Ticket
from classes.crew import Crew
class Airplane:
    def __init__(self, id: int, capacity: List[Ticket]):
        def check_id(elem: Ticket):
            return elem.id == id
        self.capacity = list(filter(check_id, capacity))
        self.passengers: List = []
        self.id = id
        self.fuel= 0
        self.tickets = capacity
    def refuel(self):
        try:
            self.fuel += 1000
        except Exception as e:
            print(f"Возникла ошибка при заправке самолета: {e}")
            return None
        return self.fuel
    def takeoff(self, crew: Crew):
        if self.fuel > 1000 and len(self.passengers) > 0 and crew.safety_is_checked and crew.route_is_planned:
            print("Взлетаем!")
            return True
        else:
            print("Недостаточно топлива или пустой самолет!")
            return False
    def land(self):
        for p in self.passengers:
            if not p.is_serviced:
                print("Не все пассажиры обслужены, не садимся")
                return False
        print("Садимся!")
        return True
    def log_info(self):
        print(f"ID: {self.id}")
        print(f"Capacity: {len(self.capacity)-1}")
        print(f"Fuel: {self.fuel}")
        print("Passengers: ")
        for p in self.passengers:
            print(p.name)


остальные классы реализованы подобным образом
интерфейс для пользователя:
from classes.ticket import Ticket
from classes.airplane import Airplane
from classes.passenger import Passenger
from classes.crew import Crew
from classes.service import Service
from classes.runway import Runway

def check(input_str):
    if input_str.strip() == '':
        print("Ошибка: введена пустая строка. Попробуйте еще раз.")
        return False
    else:
        return True
    
def input_check(text):
    while True:
        user_input = input(text)
        if check(user_input):
            return user_input

def print_menu():
    print("Выберите действие:")
    print("1. Создать самолет")
    # print("2. Создать билет")
    print("3. Создать пассажира")
    print("4. Операция регистрации на рейс")
    print("5. Операция взлета")
    print("6. Операция обслуживания пассажиров в полете")
    print("7. Операция планирования маршрутов")
    print("8. Операция обеспечения безопасности")
    print("9. Операция заправки самолета")
    print("10. Информация о выбранном самолете")
    print("11. Операция посадки")
    print("0. Выход")

def create_airplane(airplanes):
    id = input_check("Введите идентификатор самолета: ")
    capacity = int(input_check("Введите вместимость самолета: "))
    tickets = [Ticket(i + 1, id) for i in range(capacity)]
    airplane = Airplane(id, tickets)
    airplanes.append(airplane)
    print("Самолет успешно создан.")

# def create_ticket(tickets):
#     number = input_check("Введите номер билета: ")
#     id = input_check("Введите идентификатор самолета: ")
#     ticket = Ticket(number, id)
#     tickets.append(ticket)
#     print("Билет успешно создан.")

def create_passenger(passengers):
    name = input_check("Введите имя пассажира: ")
    passenger = Passenger(name)
    passengers.append(passenger)
    print("Пассажир успешно создан.")

def register_passenger(passenger, airplane):
    print(airplane.tickets[0].number)
    ticket_number = int(input_check("Введите номер билета: "))
    ticket = next((t for t in airplane.tickets if t.number == ticket_number), None)
    if ticket:
        passenger.register(ticket, airplane)
        print("Пассажир успешно зарегистрирован на рейс.")
    else:
        print("Билет не найден.")

def takeoff(airplane, crew):
    #airplane.log_info()
    #crew.log_info()
    airplane.takeoff(crew)

def land(airplane):
    #airplane.log_info()
    airplane.land()

def service_passengers(service, passengers):
    service.do_service(passengers)
    print("Пассажиры обслужены.")

def plan_route(crew, runway):
    destination = input_check("Введите пункт назначения: ")
    dep_point = input_check("Введите пункт отправления: ")
    dep_time = input_check("Введите время отправления: ")
    min_runway_length = input_check("Введите минимальную длину взлетно-посадочной полосы: ")

    crew.plan_route(destination, dep_point, dep_time, min_runway_length, runway)
    print("Маршрут запланирован.")

def ensure_safety(crew):
    crew.ensure_safety()
    print("Безопасность проверена.")

def refuel(airplane):
    airplane.refuel()
    print("Самолет заправлен.")

def log_info_airplane(airplane):
    airplane.log_info()

def main():
    airplanes = []
    tickets = []
    passengers = []
    service = Service()
    runway = Runway()
    crew = Crew()

    while True:
        print_menu()
        choice = input_check("Введите номер действия: ")
        if choice == "1":
            create_airplane(airplanes)
        # elif choice == "2":
            # create_ticket(tickets)
        elif choice == "3":
            create_passenger(passengers)
        elif choice == "4":
            if len(airplanes) == 0:
                print("Сначала создайте самолет.")
            else:
                passenger = None
                while passenger is None:
                    passenger_name = input_check("Введите имя пассажира: ")
                    for p in passengers:
                        if p.name == passenger_name:
                            passenger = p
                            break

                    if passenger is None:
                        print("Пассажир не найден.")

                airplane = None
                while airplane is None:
                    airplane_id = input_check("Введите идентификатор самолета: ")
                    for a in airplanes:
                        if a.id == airplane_id:
                            airplane = a
                            break

                    if airplane is None:
                        print("Самолет не найден.")

                register_passenger(passenger, airplane)
        elif choice == "5":
            if len(airplanes) == 0:
                print("Сначала создайте самолет.")
            else:
                crew.log_info()
                airplanes[0].takeoff(crew)
        elif choice == "11":
            airplanes[0].land()
        elif choice == "6":
            if len(passengers) == 0:
                print("Сначала создайте пассажиров.")
            else:
                service_passengers(service, passengers)
        elif choice == "7":
            plan_route(crew, runway)
        elif choice == "8":
            ensure_safety(crew)
        elif choice == "9":
            if len(airplanes) == 0:
                print("Сначала создайте самолет.")
            else:
                refuel(airplanes[0])
        elif choice == "10":
            airplane_id = input("Введите id самолета: ")
            for airplane in airplanes:
                if airplane.id == airplane_id:
                    log_info_airplane(airplane)
        elif choice == "0":
            break
        else:
            print("Некорректный ввод. Попробуйте ещё раз.")

if __name__ == "__main__":
    main()



вот так выглядит интерфейс в консоли:
![image](https://github.com/NikitaZotov/ppois-2-2024/assets/100913385/06104603-87aa-4d3f-8cb8-a9a43bba9209)
