import random
import tempfile
import uuid

import pytest
from faker import Faker
from result import is_err

from src.core.employee import Employee
from src.core.repository.database import SQLiteRepository


@pytest.fixture
def temp_db_file():
    with tempfile.NamedTemporaryFile(suffix=".db") as temp_db:
        yield temp_db.name


def generate_random_employee() -> Employee:
    faker = Faker()
    return Employee(
        id=uuid.uuid4(),
        name=faker.name(),
        age=random.randint(18, 100),
        position=faker.job(),
        salary=round(random.uniform(30000, 120000), 2)
    )

@pytest.fixture
def employee_repo(temp_db_file):
    table_name = "employee"
    create_table_sql = f"""
    CREATE TABLE {table_name} (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER CHECK(age >= 18),
        position TEXT,
        salary REAL CHECK(salary > 0)
    );
    """
    repo = SQLiteRepository(
        cls=Employee,
        db_path=temp_db_file,
        table_name=table_name,
        create_sql=create_table_sql
    )
    print(repo.get_list())
    print("end creation")
    return repo


class TestSQLiteRepository:

    def test_add(self, employee_repo):
        employee = generate_random_employee()
        employee_repo.add(employee)

        result = employee_repo.get(employee.id)
        assert result is not None
        assert result.id == employee.id
        assert result.name == employee.name
        assert result.age == employee.age
        assert result.position == employee.position
        assert result.salary == employee.salary

    def test_list(self, employee_repo):
        num_employees = 10
        for i in range(num_employees):
            employee = generate_random_employee()
            employee_repo.add(employee)
        result = employee_repo.get_list()
        assert result is not None
        assert len(result) == num_employees

    def test_get(self, employee_repo):
        employee = generate_random_employee()
        employee_repo.add(employee)
        employee2 = employee_repo.get(employee.id)
        assert employee2.id == employee.id
        assert employee2.name == employee.name
        assert employee2.salary == employee.salary

    def test_update(self, employee_repo):
        employee = generate_random_employee()
        employee_repo.add(employee)
        new_age = employee.age + 1
        new_salary = employee.salary + 1000.0
        new_position = "Designer middle"
        employee_repo.update(employee.id, age=new_age, position=new_position, salary=new_salary)
        employee_updated = employee_repo.get(employee.id)
        assert employee_updated.age == new_age
        assert employee_updated.salary == new_salary
        assert employee_updated.position == new_position

    def test_remove(self, employee_repo):
        employee = generate_random_employee()
        employee_repo.add(employee)
        employee_repo.remove(employee.id)
        employees = employee_repo.get_list()
        assert len(employees) == 0

    def test_find(self, employee_repo):
        employee = generate_random_employee()
        employee_repo.add(employee)
        employee_found = employee_repo.find(key="name", value=employee.name)[0]
        assert employee_found.id == employee.id
        assert employee_found.name == employee.name


    def test_fail_add_duplicate(self, employee_repo):
        employee = generate_random_employee()
        employee_repo.add(employee)
        res = employee_repo.add(employee)
        assert is_err(res) == True
        assert "unique constraint failed" in res.err_value.lower()
