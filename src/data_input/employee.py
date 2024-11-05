from uuid import UUID

from pydantic import ValidationError
from result import Result, Ok, Err

from src.data_input.serializers import CreateEmployeeData, UpdateEmployeeData


def input_employee_id() -> UUID:
    employee_id = input("Введите id сотрудника: ")
    return UUID(employee_id)


def input_create_employee_data() -> CreateEmployeeData:
    data = {}
    while True:
        try:
            data["name"] = input("Введите имя: ") if data.get("name") is None else data.get("name")
            data["age"] = int(input("Введите возраст: ")) if data.get("age") is None else data.get("age")
            data["position"] = input("Введите должность: ") if data.get("position") is None else data.get("position")
            data["salary"] = float(input("Введите зарплату: ")) if data.get("salary") is None else data.get("salary")
            return CreateEmployeeData.model_validate(data)
        except ValidationError as e:
            for err in e.errors():
                print(f"{err['loc'][0]}: {err['msg']}")
                data[err['loc'][0]] = None


def input_employee_name():
    return input("Введите имя: ")


def input_update_employee_data() -> Result[UpdateEmployeeData, str]:
    data = {}
    keys = ["name", "age", "position", "salary"]
    ru_names = {"name": "имя", "age": "возраст", "position": "должность", "salary": "зарплата"}
    while True:
        try:
            for key in keys:
                val = input(f"Введите {ru_names[key]}, если хотите обновить: ")
                if val:
                    data[key] = val
            if not any(data.values()):
                return Err("Нечего обновлять")
            return Ok(UpdateEmployeeData.model_validate(data))
        except ValidationError as e:
            keys = []
            for err in e.errors():
                print(f"{err['loc'][0]}: {err['msg']}")
                keys.append(err['loc'][0])