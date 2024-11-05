import sqlite3
from uuid import UUID
from contextlib import contextmanager
from sqlite3 import Cursor, DatabaseError
from typing import TypeVar, Generic, Iterator, Type

from pydantic import BaseModel
from result import Result, Err, Ok

from src.core.repository.abstract import IRepository

T = TypeVar('T', bound=BaseModel)


class SQLiteRepository(IRepository[T], Generic[T]):

    def __init__(self, cls: Type[T], db_path: str, table_name: str, create_sql: str):
        super().__init__(cls)
        self.db_path = db_path
        self.table_name = table_name
        self.create_table(create_sql)

    @contextmanager
    def connect(self) -> Iterator[Cursor]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            yield conn.cursor()

    def create_table(self, sql: str):
        with self.connect() as cursor:
            cursor.execute(sql)

    def add(self, item: T) -> Result[None, str]:
        try:
            with self.connect() as cursor:
                query = """SELECT name FROM sqlite_master WHERE type='table';"""
                cursor.execute(query)
                columns_list = item.model_dump().keys()
                columns = ", ".join(columns_list)
                values_list = item.model_dump().values()
                values = tuple(map(lambda x: str(x) if isinstance(x, UUID) else x, values_list))
                placeholders = ", ".join("?" * len(values))
                cursor.execute(f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})", values)
                cursor.connection.commit()
                return Ok(None)
        except DatabaseError as e:
            return Err(str(e))

    def get(self, item_id: UUID) -> T | None:
        with self.connect() as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id=?", (str(item_id), ))
            row = cursor.fetchone()
            return self._to_obj(row) if row else None

    def get_list(self):
        with self.connect() as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            return self._to_obj_list(cursor.fetchall())

    def remove(self, item_id: UUID):
        with self.connect() as cursor:
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id=?", (str(item_id), ))
            cursor.connection.commit()

    def update(self, item_id: UUID, **params):
        with self.connect() as cursor:
            placeholders = ", ".join([f"{key} = ?" for key in params])
            values = (*params.values(), str(item_id))
            cursor.execute(f"UPDATE {self.table_name} SET {placeholders}WHERE id=?", values)
            cursor.connection.commit()

    def find(self, key, value) -> list[T]:
        with self.connect() as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE {key}=?", (value, ))
            return self._to_obj_list(cursor.fetchall())

    def _to_obj(self, db_item):
        return self.cls(**dict(db_item))

    def _to_obj_list(self, db_items):
        return list(map(lambda x: self._to_obj(x), db_items))
