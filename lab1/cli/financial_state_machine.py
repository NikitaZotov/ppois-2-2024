from statemachine import State
from statemachine import StateMachine

from model.entities.bank import Bank
from model.entities.card_owner import CardOwner
from model.entities.credit_card import CreditCard
from model.services.finances_service import FinancesService
from model.entities.finance_exceptions import FinanceException
import helper


class FinancialStateMachine(StateMachine):
    view_banks = State(initial=True)
    view_bank = State()
    create_bank = State()
    delete_bank = State()
    view_card = State()
    create_card = State()
    delete_card = State()
    view_balance = State()
    deposit = State()
    withdraw = State()
    pay = State()
    transfer = State()
    change_pin = State()
    change_limit = State()
    toggle_block = State()
    exit_ = State(final=True)

    move_next = (
            exit_.from_(view_banks, cond="navigating_backwards")

            | view_banks.from_(view_bank, cond="navigating_backwards")
            | view_banks.to(view_bank, cond="navigating_by_index")

            | view_bank.from_(view_card, cond="navigating_backwards")
            | view_card.from_(view_bank, cond="navigating_by_index")

            | view_banks.to(create_bank, cond="navigating_create")
            | view_banks.from_(create_bank)

            | view_bank.from_(create_card)
            | view_bank.to(create_card, cond="navigating_create")

            | view_bank.to(delete_bank, cond="navigating_delete")
            | view_banks.from_(delete_bank)

            | view_card.to(view_balance, cond="navigating_balance")
            | view_card.from_(view_balance)

            | view_card.to(delete_card, cond="navigating_delete")
            | view_bank.from_(delete_card)

            | view_card.to(withdraw, cond="navigating_withdraw")
            | view_card.from_(withdraw)

            | view_card.to(deposit, cond="navigating_deposit")
            | view_card.from_(deposit)

            | view_card.to(transfer, cond="navigating_transfer")
            | view_card.from_(transfer)

            | view_card.to(pay, cond="navigating_pay")
            | view_card.from_(pay)

            | view_card.to(toggle_block, cond="navigating_toggle_block")
            | view_card.from_(toggle_block)

            | view_card.to(change_limit, cond="navigating_limit")
            | view_card.from_(change_limit)

            | view_card.to(change_pin, cond="navigating_pin")
            | view_card.from_(change_pin)

            # in case user enters invalid transition
            | view_card.to.itself(internal=True)
            | view_bank.to.itself(internal=True)
            | view_banks.to.itself(internal=True)
    )

    def __init__(self, finances_service: FinancesService):
        self.__finances_service: FinancesService = finances_service
        self.__selected_bank: Bank | None = None
        self.__selected_card: CreditCard | None = None
        self.__selected_index: int = 0
        super().__init__()

    def run(self):
        while True:
            self.move_next(input())

    def navigating_backwards(self, input_: str) -> bool:
        return input_ == 'q'

    def navigating_balance(self, input_: str) -> bool:
        return input_ == 'bal'

    def navigating_pay(self, input_: str) -> bool:
        return input_ == 'pay'

    def navigating_withdraw(self, input_: str) -> bool:
        return input_ == 'wdr'

    def navigating_deposit(self, input_: str) -> bool:
        return input_ == 'dep'

    def navigating_pin(self, input_: str) -> bool:
        return input_ == 'pin'

    def navigating_toggle_block(self, input_: str) -> bool:
        return input_ == 'blc'

    def navigating_limit(self, input_: str) -> bool:
        return input_ == 'lim'

    def navigating_transfer(self, input_: str) -> bool:
        return input_ == 'trs'

    def navigating_create(self, input_: str) -> bool:
        return input_ == 'c'

    def navigating_delete(self, input_: str) -> bool:
        return input_ == 'd'

    def navigating_by_index(self, input_: str) -> bool:
        if input_.isnumeric():
            self.__selected_index = int(input_)
            return True
        return False

    def on_enter_view_banks(self) -> None:
        self.__selected_bank = None
        print("List of all banks.\nPress q to exit, c to add new bank, number to view bank")
        banks = self.__finances_service.get_banks()

        for i, bank in enumerate(banks):
            print(f"{i} - {bank.name}")

    def on_enter_create_bank(self) -> None:
        bank_name = input("Input bank name")

        try:
            _ = self.__finances_service.create_bank(bank_name)
            print("Bank created")
        except Exception as e:
            print(str(e))
        finally:
            self.move_next()

    def on_enter_create_card(self) -> None:
        card_number = helper.input_numeric("Input card number")
        card_owner = CardOwner('Sample name', 'Sample address', None, 'Sample phone')
        card_pin: int = helper.input_numeric("PIN")

        try:
            _ = self.__finances_service.create_card(self.__selected_bank.name, card_number, card_owner, card_pin)
            print("Card created")
        except Exception as e:
            print(str(e))
        finally:
            self.move_next()

    def on_enter_view_card(self) -> None:
        try:
            if self.__selected_card is None:
                self.__selected_card = self.__finances_service.get_cards(self.__selected_bank.name)[self.__selected_index]

            print("Card information.\nPress q to return, bal to check balance, trs to transfer,\n"
                  "wdr to withdraw, Pay to pay, blc to toggle block of card,\n"
                  "dep to deposit, pin to change pin, lim to change limit, del to delete card")
            print(self.__selected_card.card_number)
            print(self.__selected_card.owner.name)
            if self.__selected_card.is_blocked():
                print("BLOCKED")
        except IndexError:
            print("Invalid index")
            self.move_next('q')

    def on_enter_view_bank(self) -> None:
        self.__selected_card = None
        try:
            if self.__selected_bank is None:
                self.__selected_bank = self.__finances_service.get_banks()[self.__selected_index]

            print(f"{self.__selected_bank.name} information.\nPress q to return, d to delete bank,\n"
                  f"c to add new card, number to view card")
            cards = self.__finances_service.get_cards(self.__selected_bank.name)
            for i, card in enumerate(cards):
                print(f"{i} - {card.card_number}; {card.owner.name}")
        except IndexError:
            print("Invalid index")
            self.move_next('q')

    def on_enter_delete_bank(self) -> None:
        print("Deleting bank")
        self.__finances_service.remove_bank(self.__selected_bank.name)
        self.__selected_bank = None
        self.move_next()

    def on_enter_delete_card(self) -> None:
        print("Deleting card")
        self.__finances_service.remove_card(self.__selected_bank.name, self.__selected_card.card_number)
        self.__selected_card = None
        self.move_next()

    def on_enter_withdraw(self) -> None:
        input_amount: int = helper.input_numeric("withdraw amount")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.__finances_service.withdraw(self.__selected_bank.name, self.__selected_card.card_number,
                                             input_amount, input_pin)
            print("Withdrawal successful")
        except FinanceException as e:
            print(str(e))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_view_balance(self) -> None:
        input_pin: int = helper.input_numeric("PIN")

        try:
            balance: int = self.__finances_service.get_balance(self.__selected_bank.name,
                                                               self.__selected_card.card_number, input_pin)
            print(f"Balance: {balance}")
        except FinanceException as e:
            print(str(e))
        finally:
            self.move_next()

    def on_enter_deposit(self) -> None:
        input_amount: int = helper.input_numeric("deposit amount")

        try:
            self.__finances_service.deposit(self.__selected_bank.name, self.__selected_card.card_number, input_amount)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_pay(self) -> None:
        input_amount: int = helper.input_numeric("pay amount")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.__finances_service.pay(self.__selected_bank.name, self.__selected_card.card_number,
                                        input_amount, input_pin)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_transfer(self) -> None:
        input_receiver: int = helper.input_numeric("receiver card number")
        input_amount: int = helper.input_numeric("transfer amount")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.__finances_service.transfer(self.__selected_bank.name, self.__selected_card.card_number,
                                             input_receiver, input_pin, input_amount)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_toggle_block(self) -> None:
        self.__finances_service.toggle_block(self.__selected_bank.name, self.__selected_card.card_number)

        if self.__selected_card.is_blocked():
            print("Card blocked")
        else:
            print("Card unblocked")

        self.move_next()

    def on_enter_change_limit(self) -> None:
        input_amount: int = helper.input_numeric("payment limit")
        input_pin: int = helper.input_numeric("PIN")

        try:
            self.__finances_service.set_limit(self.__selected_bank.name, self.__selected_card.card_number,
                                              input_amount, input_pin)
        except FinanceException as fe:
            print(str(fe))
        except ValueError as e:
            print(str(e))

        self.move_next()

    def on_enter_change_pin(self) -> None:
        input_pin: int = helper.input_numeric("new PIN")

        try:
            self.__finances_service.set_pin(self.__selected_bank.name, self.__selected_card.card_number, input_pin)
        except ValueError as e:
            print(str(e))
        finally:
            self.move_next()

    def before_move_next(self):
        print()

    def on_enter_exit_(self):
        print("Goodbye.")
        self.__finances_service.commit_changes()
        exit()
