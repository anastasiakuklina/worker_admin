from uuid import UUID
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IRepository(Generic[T], ABC):

    def __init__(self, cls):
        self.cls = cls

    @abstractmethod
    def add(self, item: T):
        pass

    @abstractmethod
    def get_list(self) -> list[T]:
        pass

    @abstractmethod
    def get(self, item_id: UUID) -> T | None:
        pass

    @abstractmethod
    def find(self, key, value) -> list[T]:
        pass

    @abstractmethod
    def remove(self, item_id: UUID):
        pass

    @abstractmethod
    def update(self, item_id: UUID, **params):
        pass
