from models.sample import Sample
from models.samples import Samples

s1=Sample("S1","White Flora Charm", 36,10000)
s2=Sample("S2","Yellow Daisy Garden",30,20000)
s3=Sample("S3","Silver Ribbon Dew",25,5000)
s4=Sample("S4","Ocean Pearl Dream",40,3000)
s5=Sample("S5","Purple Amethyst Glaze",36,400)
s6=Sample("S6","Pink Crystal Fairy",36,4500)
s7=Sample("S7","Sparkling Starlight",37,5000)
s8=Sample("S8","Green Matcha Muse",36,7000)
s9=Sample("S9","Sunny Side Up",29,6500)
s10=Sample("S10","Winter Snowman",30,3402)
s11=Sample("S11","Cosmic Marble Pink",36,8000)
s12=Sample("S12","Butterfly Garden Glow",36,3420)
s13=Sample("S13","Inimalist Red Ribbon",30,999)
s14=Sample("S14","Creamy Heart Pearl",32,9201)
lp=Samples()
for it in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14]:
    lp.add_item(it)
file_name="../datasets/samples.json"
lp.export_json(file_name)
lp.import_json("../datasets/samples.json")
print("List of Sample:")
lp.print_items()