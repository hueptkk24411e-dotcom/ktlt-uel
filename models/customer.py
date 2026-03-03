class Customer:
    def __init__(self,CustomerUserName=None,PhoneNumber=None,Type=None):
        self.CustomerUserName=CustomerUserName
        self.PhoneNumber=PhoneNumber
        self.Type=Type
    def __str__(self):
        infor=f"{self.CustomerUserName}\t{self.PhoneNumber}\t{self.Type}"
        return infor