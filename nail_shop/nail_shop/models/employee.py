class Employee:
    def __init__(self, emp_id=None, name=None, experience=None):
        self.emp_id = emp_id
        self.name = name
        self.experience = experience  # years (int)

    def __str__(self):
        return f"{self.emp_id}\t{self.name}\t{self.experience}"
