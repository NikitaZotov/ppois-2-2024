import random

from flask import render_template, request, redirect

from web_app import WebApp

from model.BankAccount import BankAccount
from model.Transaction import Transaction
from model.Investment import Investment
from model.FinanclialManagementSystem import FinancialManagementSystem
from model.Report import Report

from controller.file_repository import FileRepository


class WebController:
    def __init__(self, web_app: WebApp):
        self.web_app = web_app
        self.file_repo = FileRepository()

        load_data: dict = self.file_repo.load()
        self.financial_inf_system: FinancialManagementSystem = load_data['financial_inf_system']
        self.bank_account: BankAccount = load_data['bank_account']
        self.operations_count: int = load_data['operations']

        # error pages
        self.web_app.add_route(route='/error_input', handler_func=self.error_input, methods=['GET'])
        self.web_app.add_route(route='/error_not_enough_money', handler_func=self.error_not_enough_money, methods=['GET'])
        self.web_app.add_route(route='/no_investments', handler_func=self.no_investments, methods=['GET'])

        # operations pages
        self.web_app.add_route(route='/', handler_func=self.main_page, methods=['GET'])
        self.web_app.add_route(route='/make_transaction', handler_func=self.make_transaction, methods=['GET', 'POST'])
        self.web_app.add_route(route='/make_investment', handler_func=self.make_investment, methods=['GET', 'POST'])
        self.web_app.add_route(route='/make_withdrawal', handler_func=self.make_withdrawal, methods=['GET', 'POST'])
        self.web_app.add_route(route='/make_deposit', handler_func=self.make_deposit, methods=['GET', 'POST'])
        self.web_app.add_route(route='/get_analysis', handler_func=self.get_analysis, methods=['GET'])
        self.web_app.add_route(route='/get_financial_report', handler_func=self.get_financial_report, methods=['GET'])
        self.web_app.add_route(route='/form_new_budget', handler_func=self.form_new_budget, methods=['GET', 'POST'])
        self.web_app.add_route(route='/portfolio_management', handler_func=self.portfolio_management, methods=['GET', 'POST'])

    def run(self):
        self.web_app.run()

    def update(self):
        self.operations_count += 1
        if self.operations_count % 3 == 0:
            investments = self.bank_account.get_investment_portfolio().get_investments()
            if len(investments) > 0:
                index = random.randint(0, len(investments) - 1)
                investments[index].risk_changing(bool(random.randint(0, 1)))
                investments[index].profit_ratio_changing(bool(random.randint(0, 1)))
                if investments[index].get_risk() >= 1.:
                    self.bank_account.investment_removing(investments[index])

        self.file_repo.save(self.bank_account, self.financial_inf_system, self.operations_count)

    @staticmethod
    def main_page():
        return render_template('index.html')

    @staticmethod
    def error_input():
        return render_template('error_input.html')

    @staticmethod
    def error_not_enough_money():
        return render_template('error_not_enough_money.html')

    @staticmethod
    def no_investments():
        return render_template('no_investments.html')

    def make_transaction(self):
        if request.method == 'POST':
            number: int = int(request.form['transaction_number'])
            money_amount: int = int(request.form['money_amount'])
            if 1 <= number <= 8:
                transaction: Transaction = self.financial_inf_system.get_possible_transactions()[number - 1]
                try:
                    completed: bool = self.bank_account.get_balance() > money_amount

                    self.bank_account.make_transaction(transaction, money_amount)

                    self.update()
                    return redirect('/') if completed else redirect('/error_not_enough_money')
                except ValueError:
                    return redirect('/error_input')
            else:
                return redirect('/error_input')
        else:
            transactions: list[Transaction] = self.financial_inf_system.get_possible_transactions()
            return render_template('make_transaction.html', transactions=enumerate(transactions))

    def make_investment(self):
        if request.method == 'POST':
            number: int = int(request.form['investment_number'])
            money_amount: int = int(request.form['money_amount'])
            if 1 <= number <= 7 or money_amount <= 0:
                investment: Investment = self.financial_inf_system.get_possible_investments()[number - 1]
                if self.bank_account.get_balance() < money_amount:
                    return redirect('/error_not_enough_money')
                else:
                    self.bank_account.make_investment(investment, money_amount)

                    self.update()
                    return redirect('/')
            else:
                return redirect('/error_input')
        investments: list[Investment] = self.financial_inf_system.get_possible_investments()
        return render_template('make_investment.html', investments=enumerate(investments))

    def make_withdrawal(self):
        if request.method == 'POST':
            money_amount: int = int(request.form['money_amount'])
            try:
                completed: bool = self.bank_account.get_balance() > money_amount

                self.bank_account.withdrawal(money_amount)

                self.update()
                return redirect('/') if completed else redirect('/error_not_enough_money')
            except ValueError:
                return redirect('/error_input')
        return render_template('make_withdrawal.html')

    def make_deposit(self):
        if request.method == 'POST':
            money_amount: int = int(request.form['money_amount'])
            try:
                self.bank_account.deposit(money_amount)

                self.update()
                return redirect('/')
            except ValueError:
                return redirect('/error_input')
        return render_template('make_deposit.html')

    def get_analysis(self):
        report: Report = self.bank_account.get_analysis()
        return render_template('get_analysis.html', text=report.get_text().split(';'))

    def get_financial_report(self):
        report: Report = self.bank_account.get_financial_report()
        return render_template('get_financial_report.html', text=report.get_text().split(';'))

    def form_new_budget(self):
        if request.method == 'POST':
            self.bank_account.form_new_budget()

            self.update()
            return redirect('/')
        else:
            return render_template('form_new_budget.html')

    def portfolio_management(self):
        if request.method == 'POST':
            number: int = int(request.form['investment_number'])
            print(123)
            investments: list[Investment] = self.bank_account.get_investment_portfolio().get_investments()
            operation_key: str = request.form['operation_key']

            if 1 <= number <= len(investments):
                investment: Investment = investments[number - 1]

                if 1 <= int(operation_key) <= 5:
                    self.bank_account.portfolio_management(investment, operation_key)

                    self.update()
                    return redirect('/')
                else:
                    return redirect('/error_input')
            else:
                return redirect('/error_input')
        else:
            investments: list[Investment] = self.bank_account.get_investment_portfolio().get_investments()

            if len(investments) > 0:
                return render_template('portfolio_management.html', investments=enumerate(investments))
            else:
                return redirect('/no_investments')
