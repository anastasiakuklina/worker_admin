from .abstract import ICommand
from src.core.employee import SQLiteEmployeeRepository


class FindByNameCommand(ICommand):

    def __init__(self, repository: SQLiteEmployeeRepository, name: str):
        self.repository = repository
        self.name = name

    def execute(self):
        return self.repository.find_by_name(self.name)