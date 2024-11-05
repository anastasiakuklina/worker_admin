from uuid import UUID

from pydantic import ValidationError
from result import Result, Ok, Err

from src.data_input.serializers import CreateEmployeeData, UpdateEmployeeData


def input_employee_id() -> UUID:
    employee_id = input("Введите id сотрудника: ")
    return UUID(employee_id)

EMPLOYEE_FIELDS = {"name": "имя", "age": "возраст", "position": "должность", "salary": "зарплата"}


def input_create_employee_data() -> CreateEmployeeData:
    data = {}
    while True:
        try:
            for key, value in EMPLOYEE_FIELDS.items():
                if not key in data:
                    data[key] = input(f"Введите {value}: ")
            return CreateEmployeeData.model_validate(data)
        except ValidationError as e:
            for err in e.errors():
                key = str(err['loc'][0])
                print(f"{key}: {err['msg']}")
                data.pop(key)


def input_employee_name():
    return input("Введите имя: ")


def input_update_employee_data() -> Result[UpdateEmployeeData, str]:
    data = {}
    keys = list(EMPLOYEE_FIELDS.keys())
    while True:
        try:
            for key in keys:
                value = input(f"Введите {EMPLOYEE_FIELDS[key]}, если хотите обновить: ")
                if value:
                    data[key] = value
            if not data:
                return Err("Нечего обновлять")
            return Ok(UpdateEmployeeData.model_validate(data))
        except ValidationError as e:
            keys = []
            for err in e.errors():
                key = str(err['loc'][0])
                print(f"{key}: {err['msg']}")
                keys.append(key)