import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.customer import Customer
from models.customers import Customers

# 4 cases:
#   Nguyen An  — VIP, có feedback
#   Tran Binh  — Normal, có feedback
#   Le Chau    — Normal, KHÔNG có feedback (None)
#   Pham Duc   — VIP, KHÔNG có feedback (chuỗi rỗng "")

customers = [
    Customer("Nguyen An",  "0901111111", "VIP",    5, "Very satisfied, will come back!"),
    Customer("Tran Binh",  "0902222222", "Normal", 4, "Good service, loved the design."),
    Customer("Le Chau",    "0903333333", "Normal", 3, None),
    Customer("Pham Duc",   "0904444444", "VIP",    5, ""),
]

lc = Customers()
for c in customers:
    lc.add_item(c)

os.makedirs("../datasets", exist_ok=True)
lc.export_json("../datasets/customers.json")
lc.print_items()
print(f"Done: customers.json — {len(customers)} customers")
