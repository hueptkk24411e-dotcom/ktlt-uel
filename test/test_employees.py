from models.employee import Employee
from models.employees import Employees

e1=Employee("meo","Mèo",111,1,"teo")
e2=Employee("ga","Gà",333,2,"ty")
e3=Employee("gau","Gấu",5444,1,"bin")
e4=Employee("chon","Chồn",6555,3,"bo")
e5=Employee("chuot","Chuột",7446,4,"tuan")
emp=Employees()
emp.add_items([e1,e2,e3,e4,e5])
print("List of Employees:")
emp.print_items()
print("Export Customer to JSON FILE:")
emp.export_json("../datasets/employees.json")