import sys, os

from nail_shop.nail_shop.models.sample import Sample
from nail_shop.nail_shop.models.samples import Samples

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



samples = [
    Sample("S01", "White Flora Charm",     36, "Spring"),
    Sample("S02", "Yellow Daisy Garden",   30, "Spring"),
    Sample("S03", "Silver Ribbon Dew",     25, "Spring"),
    Sample("S04", "Pink Crystal Fairy",    40, "Summer"),
    Sample("S05", "Sparkling Starlight",   37, "Summer"),
    Sample("S06", "Green Matcha Muse",     36, "Autumn"),
    Sample("S07", "Sunny Side Up",         26, "Autumn"),
    Sample("S08", "Butterfly Garden Glow", 36, "Autumn"),
    Sample("S09", "Ocean Pearl Dream",     40, "Winter"),
    Sample("S10", "Winter Snowman",        30, "Winter"),
    Sample("S11", "Purple Amethyst Glaze", 36, "Winter"),
    Sample("S12", "Creamy Heart Pearl",    32, "Summer"),
    Sample("S13", "Inimalist Red Ribbon",  30, "Autumn"),
    Sample("S14", "Cosmic Marble Pink",    36, "Summer"),
]

ls = Samples()
for s in samples:
    ls.add_item(s)

os.makedirs("../datasets", exist_ok=True)
ls.export_json("../datasets/samples.json")
ls.print_items()
print("Done: samples.json")
