from model.entities.bank import Bank
from model.entities.card_owner import CardOwner
from model.entities.credit_card import CreditCard
from model.repository.exceptions import RepositoryException
from model.repository.interfaces import Repository


class FinancesService:
    def __init__(self, repository: Repository):
        self.__banks: list[Bank] = []
        self.__repository: Repository = repository
        self.init_data()

    def get_banks(self) -> list[Bank]:
        return self.__banks.copy()

    def get_bank(self, name: str) -> Bank:
        bank = next((x for x in self.__banks if x.name == name), None)

        if bank is None:
            raise ValueError(f"Bank with name {name} not found")

        return bank

    def create_bank(self, bank_name: str) -> Bank:
        bank = next((x for x in self.__banks if x.name == bank_name), None)

        if bank is not None:
            raise ValueError(f"Bank with name {bank_name} already exists")

        new_bank = Bank(bank_name)
        self.__banks.append(new_bank)

        return new_bank

    def remove_bank(self, bank_name: str):
        to_remove = self.get_bank(bank_name)
        self.__banks.remove(to_remove)

    def get_card(self, bank_name: str, card_number: int) -> CreditCard:
        bank = self.get_bank(bank_name)
        card = bank.get_card(card_number)

        return card

    def get_cards(self, bank_name: str) -> list[CreditCard]:
        bank = self.get_bank(bank_name)
        # Already copies list inside bank class
        return bank.get_cards()

    def create_card(self, bank_name: str, card_number: int, card_owner: CardOwner, card_pin: int) -> CreditCard:
        if card_number <= 0:
            raise ValueError(f"Card number cannot be non-positive")

        bank = self.get_bank(bank_name)

        existing_card = next((x for x in bank.get_cards() if x.card_number == card_number), None)
        if existing_card is not None:
            raise ValueError(f"Card with number {card_number} already exists")

        new_card = CreditCard(card_number, card_owner, card_pin, False)
        bank.add_card(new_card)

        return new_card

    def remove_card(self, bank_name: str, card_number: int) -> None:
        bank = self.get_bank(bank_name)
        to_remove = bank.get_card(card_number)
        bank.remove_card(to_remove)

    def withdraw(self, bank_name: str, card_number: int, amount: int, card_pin: int) -> None:
        card = self.get_card(bank_name, card_number)
        card.withdraw(amount, card_pin)

    def get_balance(self, bank_name: str, card_number: int, card_pin: int) -> int:
        card = self.get_card(bank_name, card_number)
        return card.get_balance(card_pin)

    def deposit(self, bank_name: str, card_number: int, amount: int) -> None:
        card = self.get_card(bank_name, card_number)
        card.deposit(amount)

    def pay(self, bank_name: str, card_number: int, amount: int, card_pin: int) -> None:
        card = self.get_card(bank_name, card_number)
        card.pay(amount, card_pin)

    def set_limit(self, bank_name: str, card_number: int, amount: int, card_pin: int) -> None:
        card = self.get_card(bank_name, card_number)
        card.set_limit(card_pin, amount)

    def set_pin(self, bank_name: str, card_number: int, new_pin: int) -> None:
        card = self.get_card(bank_name, card_number)
        card.set_pin(new_pin)

    def transfer(self, bank_name: str, sender_card_number: int, receiver_card_number: int,
                 pin: int, amount: int) -> None:
        bank = self.get_bank(bank_name)

        sender_card = bank.get_card(sender_card_number)
        receiver_card = bank.get_card(receiver_card_number)

        bank.transfer(sender_card, receiver_card, pin, amount)

    def toggle_block(self, bank_name: str, card_number: int) -> None:
        card = self.get_card(bank_name, card_number)

        if card.is_blocked():
            card.unblock()
        else:
            card.block()

    def init_data(self) -> None:
        try:
            self.__banks = self.__repository.load()
        except RepositoryException:
            print("Couldn't load existing data. Using default values")

    def commit_changes(self) -> None:
        self.__repository.save(self.__banks)
