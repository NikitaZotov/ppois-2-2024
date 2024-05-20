import sys
sys.path.insert(1, 'D://work//BSUIR//PPOIS//Sem4//LW1//')
from model.services.finances_service import *
from model.repository.file_repository import *


class ServiceProvider:
    Repository: FileRepository = None
    FinancesService: FinancesService = None

    def __init__(self):
        if self.Repository is None:
            self.Repository = FileRepository("wannabe-db.pickle")
        if self.FinancesService is None:
            self.FinancesService = FinancesService(self.Repository)
