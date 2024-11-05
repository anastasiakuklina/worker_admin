from .abstract import ICommand
from src.core.employee import SQLiteEmployeeRepository
from src.data_input import CreateEmployeeData


class AddEmployeeCommand(ICommand):

    def __init__(self, repository: SQLiteEmployeeRepository, data: CreateEmployeeData):
        self.repository = repository
        self.data = data

    def execute(self):
        return self.repository.add_new(self.data)