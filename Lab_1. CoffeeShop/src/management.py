from typing import List

import colors
from equipment import Equipment
from exceptions import BudgetException


class Management:
    """Class of basic management of the coffee shop budget and equipment"""

    def __init__(self, budget: float = 0.0):
        self.__account: float = budget
        self.__account_history: List[dict] = []

    def income(self, amount: float) -> None:
        """Add money to the coffee shop account (accounting for operations)"""
        self.__account += amount
        self.__account_history.append({'income': amount})

    def expense(self, amount: float) -> None:
        """Withdraw money from the coffee shop account (accounting for operations)"""
        self.__account -= amount
        self.__account_history.append({'expense': amount})

    def show_history(self) -> str:
        """Show account history (accounting for operations)"""
        history: str = ''
        for operation in self.__account_history:
            for key, value in operation.items():
                if key == 'expense':
                    key_color: str = colors.CRED + key + colors.CEND
                else:
                    key_color: str = colors.CGREEN + key + colors.CEND
                history += f'{key_color}: {value}\n'
        return history

    @property
    def account(self):
        """account getter"""
        return self.__account
