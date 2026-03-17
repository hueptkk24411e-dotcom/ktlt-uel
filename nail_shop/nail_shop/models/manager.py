class Manager:
    def __init__(self, manager_id=None, name=None, username=None, password=None):
        self.manager_id = manager_id
        self.name = name
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.manager_id}\t{self.name}\t{self.username}"
