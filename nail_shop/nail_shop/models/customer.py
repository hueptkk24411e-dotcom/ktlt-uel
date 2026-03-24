class Customer:
    def __init__(self, name=None, phone=None, cus_type=None, rating=None, feedback=None):
        self.name     = name
        self.phone    = phone
        self.cus_type = cus_type   # "VIP" or "Normal"
        self.rating   = rating     # 1-5
        self.feedback = feedback   # string, có thể None

    def __str__(self):
        return f"{self.name}\t{self.phone}\t{self.cus_type}\t{self.rating}\t{self.feedback or ''}"
