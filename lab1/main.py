from cli.financial_state_machine import FinancialStateMachine
from model.services.finances_service import FinancesService
from model.repository.file_repository import FileRepository, Repository

repository: Repository = FileRepository("appstate.pickle")
finances_service = FinancesService(repository)

state_machine = FinancialStateMachine(finances_service)

state_machine.run()
