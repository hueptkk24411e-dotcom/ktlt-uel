from models.employee import Employee
from models.employees import Employees

e1=Employee("meo","Mèo",1,"teo")
e2=Employee("ga","Gà",3,"ty")
e3=Employee("gau","Gấu",5,"bin")
e4=Employee("chon","Chồn",6,"bo")
e5=Employee("chuot","Chuột",7,"tuan")
emp=Employees()
emp.add_items([e1,e2,e3,e4,e5])
print("List of Employees:")
emp.print_items()
print("Export Customer to JSON FILE:")
emp.export_json("../datasets/employees.json")