from dataclasses import asdict
from typing import TypeVar, Generic

from src.core.repository.abstract import IRepository

T = TypeVar('T')


class DictRepository(IRepository[T]):

    def __init__(self, cls):
        super().__init__(cls)
        self.repo = {}

    def add(self, item: T):
        print('2222222')
        self.repo[item.id] = asdict(item)

    def get_list(self) -> list[T]:
        return list(map(lambda item: self.cls(item), self.repo.values()))

    def get(self, i: int):
        print(self.repo)
        print(self.repo[i])
        return self.cls(**self.repo[i])


# class DictEmployeeRepository(DictRepository[Employee]):
#
#     def __init__(self):
#         super().__init__(Employee)
#
#     def add(self, item: Employee):
#         super().add(item)
#
#     def get_list(self) -> list[Employee]:
#         return super().get_list()
#
#     def get(self, i: int) -> Employee:
#         return super().get(i)