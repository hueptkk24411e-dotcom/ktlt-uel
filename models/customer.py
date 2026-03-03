class Customer:
    def __init__(self,CustomerUserName=None, Password=None, PhoneNumber=None):
        self.CustomerUserName=CustomerUserName
        self.Password=Password
        self.PhoneNumber=PhoneNumber
    def __str__(self):
        infor=f"{self.CustomerUserName}\t{self.Password}\t{self.PhoneNumber}"
        return infor