from models.employee import Employee
from models.employees import Employees
e1=Employee("E01","Anna",1111,5,"teo")
e2=Employee("E02","Lisa",3331,3,"ty")
e3=Employee("E03","Sophia",5444,4,"bin")
e4=Employee("E04","Emma",6555,6,"bo")
emp=Employees()
emp.add_items([e1,e2,e3,e4])
print("List of Employees:")
emp.print_items()
print("Export Customer to JSON FILE:")
emp.export_json("../datasets/employees.json")

