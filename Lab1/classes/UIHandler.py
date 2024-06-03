from .AuctionPlatform import AuctionPlatform
from .InputAndOutputInfo import InputAndOutputInfo
class UIHandler:

    def __init__(self):
        self.__auction_platform = None

    def menu_preparing(self):
        print("\nВыберите действие: ")
        print("\t1. Добавить лот")
        print("\t2. Добавить участника")
        print("\t3. Установить время аукциона")
        print("\t4. Информация о текущем аукционе")
        print("\t5. Начать аукцион")
        choice = input("Выберите пункт: ")
        return choice

    def choice_create_lot(self):
        print("\033[36m" + "\nВы выбрали: Добавить лот" + "\033[0m")
        lot_name = input("Введите название лота: ")
        lot_start_price = InputAndOutputInfo.numbers_input_check("Введите начальную стоимость лота: ", 10,
                                                                 1000000000000)
        print("\033[36m" + "Ставка для лота должна составлять 5-10% от начальной цены."
            + f" Для данного лота ставка может быть установлена в диапазоне от {int(lot_start_price * 5 / 100)} до {int(lot_start_price * 10 / 100)}" + "\033[0m")
        lot_bid = InputAndOutputInfo.numbers_input_check("Введите ставку лота: ", int(lot_start_price * 5 / 100),
                                                         int(lot_start_price * 10 / 100))
        self.__auction_platform.add_lot(lot_name, lot_start_price, lot_bid)
        print("\033[36m" + f"Лот \"{lot_name}\" успешно добавлен" + "\033[0m")

    def choice_create_participant(self):
        print("\033[36m" + "\nВы выбрали: Добавить участника" + "\033[0m")
        participant_name = InputAndOutputInfo.string_input_check()
        participant_money = InputAndOutputInfo.numbers_input_check("Введите сумму денег участника: ", 1, 1000000000000)
        self.__auction_platform.add_participant(participant_name, participant_money)
        print("\033[36m" + f"Участник \"{participant_name}\" успешно добавлен под номером {self.__auction_platform.count_lots()}" + "\033[0m")

    def choice_reset_timer_duration(self):
        print("\033[36m" + "\nВы выбрали: Установить время аукциона" + "\033[0m")
        print("\033[36m" + f"Максимальное время для проведения аукциона 300 секунд" + "\033[0m")
        timer_duration = InputAndOutputInfo.numbers_input_check("Введите время аукциона в секундах: ", 1, 300)
        self.__auction_platform.install_timer(timer_duration)
        print("\033[36m" + f"Время для проведения аукциона установленно на {timer_duration} секунд" + "\033[0m")

    def choice_print_information(self):
        print("\033[36m" + "\nВы выбрали: Информация о текущем аукционе" + "\033[0m")
        InputAndOutputInfo.print_info_of_auction(self.__auction_platform.count_lots(),
                                                 self.__auction_platform.count_participants(),
                                                 self.__auction_platform.time)
        InputAndOutputInfo.list_of_participants(self.__auction_platform.list_of_participants)

    def choice_run_auction(self):
        print("\033[36m" + "\nПодговка к акциону окончена" + "\033[0m")
        InputAndOutputInfo.print_info_of_auction(self.__auction_platform.count_lots(),
                                                 self.__auction_platform.count_participants(),
                                                 self.__auction_platform.time)
        InputAndOutputInfo.list_of_participants(self.__auction_platform.list_of_participants)
        if self.__auction_platform.count_lots() == 0:
            print("\033[36m" + "Аукцион не состоялся. Нет лотов  для проведения аукциона." + "\033[0m")
        elif self.__auction_platform.count_participants() == 0:
            print("\033[36m" + "Аукцион не состоялся. Нет участников для проведения аукциона." + "\033[0m")
        elif self.__auction_platform.count_participants() == 1:
            print("\033[36m" + "Аукцион не состоялся. Все лоты достаются участнику под номером 1" + "\033[0m")
        else:
            print("\033[36m" + "\nАукцион начался" + "\033[0m")
            self.auction_result()
            print("\033[36m" + "\nАукцион закончился" + "\033[0m")

    def handle_choice(self, choice):
        if choice == "1":
            self.choice_create_lot()
        elif choice == "2":
            self.choice_create_participant()
        elif choice == "3":
            self.choice_reset_timer_duration()
        elif choice == "4":
            self.choice_print_information()
        elif choice == "5":
            self.choice_run_auction()
        else:
            print("\033[31m" + "Неверный выбор. Попробуйте еще раз." + "\033[0m")

    def new_auction(self):
        while True:
            choice = input("\nХотите устроить новый аукцион?\n1. Да\n2. Нет\nВыберите пункт: ")
            if choice == "1":
                self.__auction_platform = AuctionPlatform()
                self.main_menu_loop()
            elif choice == "2":
                break
            else:
                print("\033[31m" + "Неверный выбор. Попробуйте еще раз." + "\033[0m")

    def main_menu_loop(self):
        print("\033[36m" + "\nНачало работы по подготовки к аукциону." + "\033[0m")
        while True:
            choice = self.menu_preparing()
            self.handle_choice(choice)
            if choice == "5":
                break

    def bidding_process(self, price, bid):
        last_bidder_index = None
        winner_index = None
        while True:
            InputAndOutputInfo.find_participants_for_bidding(self.__auction_platform.list_of_participants(), price + bid)
            participant_number = input("\nНомер участника, который повышает цену (для окончания нажмите enter): ")
            if participant_number == "":
                break
            else:
                participant_index = InputAndOutputInfo.find_participant(participant_number, self.__auction_platform.count_participants())
                if participant_index is not None and participant_index != last_bidder_index:
                    new_price = self.__auction_platform.__participants[participant_index].raise_price(price, bid)
                    if new_price > price:
                        print("\033[36m" + f"Текущая цена: {new_price}" + "\033[0m")
                        price = new_price
                        last_bidder_index = participant_index
                        winner_index = participant_index
                elif participant_index == last_bidder_index and last_bidder_index is not None:
                    print(
                        "\033[31m" + "Данный участник только что сделал ставку." + "\033[0m")
        winner = (winner_index, price)
        return winner

    def auction_result(self):
        self.__auction_platform.__timer.start()
        count_of_lot = self.__auction_platform.count_lots()
        while self.__auction_platform.__timer.duration > 0 and count_of_lot > 0:
            for lot_index in range(0, self.__auction_platform.count_lots()):
                print("\033[36m" + f"\nВыставляется лот {lot_index + 1}" + "\033[0m")
                InputAndOutputInfo.display_lot(self.__auction_platform.return_lot(lot_index).name, self.__auction_platform.return_lot(lot_index).start_price,
                                               self.__auction_platform.return_lot(lot_index).bid)
                current_bid = self.__auction_platform.return_lot(lot_index).bid
                current_price = self.__auction_platform.return_lot(lot_index).start_price - current_bid
                print("\033[36m" + "\nНачало торгов" + "\033[0m")
                winner = self.bidding_process(current_price, current_bid)
                print("\033[36m" + "Торги окончены." + "\033[0m")
                if winner[0] is None:
                    print("\033[36m" + f"Лот {lot_index + 1} не был продан." + "\033[0m")
                else:
                    InputAndOutputInfo.winner_announcement(winner[0] + 1, lot_index + 1, self.__auction_platform.return_lot(lot_index).name)
                    self.__auction_platform.return_participant(winner[0]).pay_money(winner[1])
                    InputAndOutputInfo.winner_paid(self.__auction_platform.return_participant(winner[0]).name,
                                                   self.__auction_platform.return_participant(winner[0]).money)
                count_of_lot -= 1
                if self.__auction_platform.__timer.duration <= 0 or count_of_lot == 0:
                    self.__auction_platform.__timer.stop()
                    break
        if count_of_lot > 0:
            print("\033[36m" + "Время аукциона вышло. Остальные лоты остались не продаными." + "\033[0m")

