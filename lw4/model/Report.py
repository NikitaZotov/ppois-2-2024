class Report:
    def __init__(self, text='Classic report without information', date='01.01.01'):
        self.__text: str = text
        self.__date: str = date

    def form_analysis_text(self, transaction_history: list = None, investments: list = None, owner_name: str = '')\
            -> None:
        if transaction_history is None:
            transaction_history: list = []
        if investments is None:
            investments: list = []
        self.__text = (f'Владелец банковского аккаунта - {owner_name}.;'
                       f'Он совершил {len(transaction_history)} транзакций:;')
        for i in transaction_history:
            if i.get_correct_operation():
                self.__text += f'\n{i.get_company_or_bank_account_number()}: {i.get_money_amount_spent()};'
            else:
                self.__text += (f'\nТранзакция {i.get_company_or_bank_account_number()}: '
                                f'{i.get_money_amount_spent()} не была завершена;')
        self.__text += f'\nА также {len(investments)} инвестиций:;'
        for i in investments:
            self.__text += (f'\n{i.get_scope_of_investment()}: {i.get_price()}, '
                            f'риск: {i.get_risk()}, прибыль: {i.get_profit_ratio()}, вложенные средства: {i.get_price()};')
        self.__text += f'\nДата: {self.__date}. Владелец Системы Крутого Управления Финансами: Карпук М.'

    def form_financial_report_text(self, balance: float = 0, transactions_amount: int = 0, investments_amount: int = 0,
                                   owner_name: str = 'Tyler') -> None:
        self.__text = (f'Владелец банковского аккаунта это {owner_name}.;'
                       f'Он совершил {transactions_amount} транзакций и '
                       f'{investments_amount} инвестиций.;На балансе на данный момент {int(balance)};')
        self.__text += f'\nДата: {self.__date}. Владелец Системы Крутого Управления Финансами: Карпук М.'

    def get_text(self) -> str:
        return self.__text
