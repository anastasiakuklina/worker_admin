from typing import TypeVar
from uuid import UUID

from src.core.commands.abstract import ICommand
from src.core.repository.abstract import IRepository

T = TypeVar('T')

class AddCommand(ICommand):

    def __init__(self, repository: IRepository, item: T):
        self.repository = repository
        self.item = item

    def execute(self):
        return self.repository.add(self.item)


class ListCommand(ICommand):

    def __init__(self, repository: IRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_list()


class UpdateCommand(ICommand):

    def __init__(self, repository: IRepository, item_id: UUID, **params):
        self.repository = repository
        self.item_id = item_id
        self.params = params

    def execute(self):
        self.repository.update(self.item_id, **self.params)


class RemoveCommand(ICommand):

    def __init__(self, repository: IRepository, item_id: UUID):
        self.repository = repository
        self.item_id = item_id

    def execute(self):
        self.repository.remove(self.item_id)
