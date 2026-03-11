from models.employee import Employee
from models.employees import Employees
e1=Employee("E01","meo",1111,1,"teo")
e2=Employee("E02","ga",3331,2,"ty")
e3=Employee("E03","gau",5444,1,"bin")
e4=Employee("E04","chon",6555,3,"bo")
e5=Employee("E05","chuot",7446,4,"tuan")
emp=Employees()
emp.add_items([e1,e2,e3,e4,e5])
print("List of Employees:")
emp.print_items()
print("Export Customer to JSON FILE:")
emp.export_json("../datasets/employees.json")

