class Customer:
    def __init__(self,CustomerUserName=None,PhoneNumber=None,Type=None,Rating=None):
        self.CustomerUserName=CustomerUserName
        self.PhoneNumber=PhoneNumber
        self.Type=Type
        self.Rating=Rating
    def __str__(self):
        infor=f"{self.CustomerUserName}\t{self.PhoneNumber}\t{self.Type}\t{self.Rating}"
        return infor