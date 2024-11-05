from result import is_ok, is_err

from src.core import ListCommand, CommandInvoker, AddCommand, FindByNameCommand, UpdateCommand
from src.core.commands.crud import RemoveCommand
from src.data_input import input_create_employee_data, input_employee_name, input_update_employee_data, \
    input_employee_id
from src.core.employee import SQLiteEmployeeRepository
from src.view import display_employees


def main() -> None:
    repository = SQLiteEmployeeRepository()
    invoker = CommandInvoker()
    while True:
        print("\nВыберите команду:")
        print("1. Добавить сотрудника")
        print("2. Удалить сотрудника")
        print("3. Обновить данные сотрудника")
        print("4. Вывести список сотрудников")
        print("5. Найти сотрудника по имени")
        print("6. Выйти")

        command = int(input("Введите команду: "))

        match command:
            case 1:
                data = input_create_employee_data()
                res = invoker.execute_command(AddCommand(repository, item=data))
                print(res.err_value) if is_err(res) else None
            case 2:
                employee_id = input_employee_id()
                invoker.execute_command(RemoveCommand(repository, employee_id))
            case 3:
                employee_id = input_employee_id()
                data = input_update_employee_data()
                if is_ok(data):
                    params = data.ok_value.model_dump(exclude_none=True)
                    invoker.execute_command(UpdateCommand(repository, employee_id, **params))
            case 4:
                employees = invoker.execute_command(ListCommand(repository))
                print(employees)
                display_employees(employees)
            case 5:
                name = input_employee_name()
                employees = invoker.execute_command(FindByNameCommand(repository, name))
                display_employees(employees)
            case 6:
                break
            case _:
                print("Команда ещё не реализована")


if __name__ == "__main__":
    # main_db()
    main()
