class Sample:
    def __init__(self, sample_id=None, name=None, price=None,  season=None):
        self.sample_id = sample_id
        self.name = name
        self.price = price        # float
        self.season = season      # "Spring" / "Summer" / "Autumn" / "Winter"

    def __str__(self):
        return f"{self.sample_id}\t{self.name}\t{self.price}\t{self.season}"
