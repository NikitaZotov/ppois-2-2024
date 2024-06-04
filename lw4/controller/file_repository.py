from model.BankAccount import BankAccount
from model.FinanclialManagementSystem import FinancialManagementSystem
import pickle


class FileRepository:
    def __init__(self):
        f: FinancialManagementSystem = FinancialManagementSystem()
        self.file_name: str = 'data_save.pickle'

    def load(self):
        with open(self.file_name, 'rb') as file:
            load_data = pickle.load(file)

        return load_data

    def save(self, bank_account: BankAccount, financial_inf_system: FinancialManagementSystem, operations_count: int):
        save_data = {
            'financial_inf_system': financial_inf_system,
            'bank_account': bank_account,
            'operations': operations_count
        }

        with open(self.file_name, 'wb') as file:
            pickle.dump(save_data, file)
