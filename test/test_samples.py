from models.sample import Sample
from models.samples import Samples

s1=Sample("S1","Name1",100,10000)
s2=Sample("S2","Name2",200,20000)
s3=Sample("S3","Name3",500,5000)
s4=Sample("S4","Name4",300,3000)
s5=Sample("S5","Name5",400,400)
s6=Sample("S6","Name6",450,4500)
s7=Sample("S7","Name7",500,5000)
s8=Sample("S8","Name8",700,7000)
s9=Sample("S9","Name9",650,6500)
s10=Sample("S10","Name10",1000,8000)
lp=Samples()
for it in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]:
    lp.add_item(it)
file_name="../datasets/samples.json"
lp.export_json(file_name)
lp.import_json("../datasets/samples.json")
print("List of Sample:")
lp.print_items()