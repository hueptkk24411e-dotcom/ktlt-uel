import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.customer import Customer
from models.customers import Customers

customers = [
    Customer("Nguyen An",  "0901111111", "VIP",    5),
    Customer("Tran Binh",  "0902222222", "Normal", 4),
    Customer("Le Chau",    "0903333333", "Normal", 3),
    Customer("Pham Duc",   "0904444444", "VIP",    5),
]

lc = Customers()
for c in customers:
    lc.add_item(c)

os.makedirs("../datasets", exist_ok=True)
lc.export_json("../datasets/customers.json")
lc.print_items()
print("Done: customers.json")
