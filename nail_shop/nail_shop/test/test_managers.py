import sys, os

from nail_shop.nail_shop.models.manager import Manager
from nail_shop.nail_shop.models.managers import Managers

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



managers = [
    Manager("M01", "Ho Tiger",   "ho",  "111111"),
    Manager("M02", "Voi Ele",    "voi", "333333"),
    Manager("M03", "Tho Trang",  "tho", "345678"),
]

lm = Managers()
for m in managers:
    lm.add_item(m)

os.makedirs("../datasets", exist_ok=True)
lm.export_json("../datasets/managers.json")
lm.print_items()
print("Done: managers.json")
