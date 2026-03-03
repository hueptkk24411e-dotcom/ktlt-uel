class Sample:
    def __init__(self,SampleID=None,SampleName=None,SamplePrice=None,SampleQuantity=None):
        self.SampleID=SampleID
        self.SampleName=SampleName
        self.SamplePrice=SamplePrice
        self.SampleQuantity=SampleQuantity
    def __str__(self):
        infor=f"{self.SampleID}\t{self.SampleName}\t{self.SamplePrice}\t{self.SampleQuantity}"
        return infor