import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.employee import Employee
from models.employees import Employees

employees = [
    Employee("E01", "Anna",   5),
    Employee("E02", "Lisa",   3),
    Employee("E03", "Sophia", 4),
    Employee("E04", "Emma",   6),
]

le = Employees()
for e in employees:
    le.add_item(e)

os.makedirs("../datasets", exist_ok=True)
le.export_json("../datasets/employees.json")
le.print_items()
print("Done: employees.json")
