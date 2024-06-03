import re
class InputAndOutputInfo:

    @staticmethod
    def print_info_of_auction(count_lots, count_participants, time):
        print(f"\nКоличество зарегистрированных лотов: {count_lots}")
        print(f"Количество зарегистрированных участников: {count_participants}")
        print(f"Установленное время аукциона: {time}")

    @staticmethod
    def display_lot(lot_name, lot_price, lot_bid):
        print(f"Имя лота: {lot_name}")
        print(f"Начальная цена: {lot_price}")
        print(f"Установленная ставка: {lot_bid}")

    @staticmethod
    def display_participant(participant_number, participant_name, participant_money):
        print(f"{participant_number}) {participant_name}, {participant_money}")

    @staticmethod
    def list_of_participants(participants):
        print(f"\nУчастники, которые зарегистрировались на аукцион: ")
        for participant in participants:
            InputAndOutputInfo.display_participant(participant.number, participant.name, participant.money)

    @staticmethod
    def find_participants_for_bidding(participants, price):
        print(f"Участники, которые могут участвовать в торгах: ")
        for participant in participants:
            if participant.money >= price:
                InputAndOutputInfo.display_participant(participant.number, participant.name, participant.money)

    @staticmethod
    def winner_announcement(winner_index, lot_index, lot_name):
        print("\033[36m" + f"\nЛот под номером {lot_index} (\"{lot_name}\") достается участнику под номером {winner_index}." + "\033[0m")

    @staticmethod
    def winner_paid(winner_name, winner_money):
        print("\033[36m" + f"{winner_name} оплачивает лот. Оставшаяся сумма: {winner_money}" + "\033[0m")

    @staticmethod
    def numbers_input_check(input_message, min_value, max_value):
        while True:
            try:
                number = int(input(input_message))
                if number <= 0:
                    print("\033[31m" + f"Данное значение должно быть больше 0." + "\033[0m")
                elif number < min_value:
                    print("\033[31m" + f"Данное значение должно быть не меньше {min_value}." + "\033[0m")
                elif number > max_value:
                    print("\033[31m" + f"Данное значение не должно превосходить {max_value}." + "\033[0m")
                else:
                    return number
            except ValueError:
                print("\033[31m" + "Ошибка: Данное значение должно быть целым числом." + "\033[0m")

    @staticmethod
    def string_input_check():
        while True:
            participant_name = input("Введите имя участника: ")
            if not re.match("^[a-zA-Z]|[а-яА-Я]|[\\s]+$", participant_name):
                print("\033[31m" + "Ошибка: Имя участника должно состоять только из букв." + "\033[0m")
            else:
                return participant_name

    @staticmethod
    def find_participant(participant_number, count_participants):
        try:
            index = int(participant_number) - 1
            if index < 0 or index >= count_participants:
                print("\033[31m" + "Ошибка: Такого участника нет." + "\033[0m")
                return None
            else:
                return index
        except ValueError:
            print("\033[31m" + "Ошибка: Номер участника должна быть числом." + "\033[0m")