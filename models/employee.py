class Employee:
    def __init__(self,EmployeeId=None, EmployeeName=None,Password=None, Experience=None, CustomerBooked=None):
        self.EmployeeId=EmployeeId
        self.EmployeeName=EmployeeName
        self.Password=Password
        self.Experience=Experience
        self.CustomerBooked=CustomerBooked
    def __str__(self):
        infor=f"{self.EmployeeId}\t{self.EmployeeName}\t{self.Experience}\t{self.CustomerBooked}"
        return infor