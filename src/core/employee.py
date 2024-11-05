import uuid
from dataclasses import dataclass

from pydantic import BaseModel

from src.data_input.serializers import CreateEmployeeData
from src.core.repository.database import SQLiteRepository


class Employee(BaseModel):
    id: uuid.UUID
    name: str
    age: int
    position: str
    salary: float


class SQLiteEmployeeRepository(SQLiteRepository[Employee]):

    def __init__(self):
        table_name = "employees"
        create_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                position TEXT,
                salary REAL
                )"""

        super().__init__(cls=Employee,
                         db_path="worker_admin.db",
                         table_name="employees",
                         create_sql=create_sql)

    def add_new(self, data: CreateEmployeeData):
        employee = Employee(id=uuid.uuid4(), **data.model_dump())
        return self.add(employee)

    def find_by_name(self, name: str):
        return super().find(key="name", value=name)
