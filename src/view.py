from src.core.employee import Employee


def display_employees(employees: list[Employee]) -> None:
    print("+--------------------------------------+------------------+---------+-----------------+----------+")
    print("| ID                                   | Имя              | Возраст | Должность       | Зарплата |")
    print("+--------------------------------------+------------------+---------+-----------------+----------+")
    for emp in employees:
        print(f"| {str(emp.id):<36} | {emp.name:<16} | {emp.age:<7} | {emp.position:<15} | {emp.salary:<8} |")
