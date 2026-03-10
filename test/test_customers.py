from models.customer import Customer
from models.customers import Customers

c1=Customer("teo","123","VIP",5)
c2=Customer("ty","234","Normal",3)
c3=Customer("bin","345","Normal",2)
c4=Customer("bo","456","Normal",4)
c5=Customer("tuan","789","VIP",5)
cus=Customers()
cus.add_items([c1,c2,c3,c4,c5])
print("List of Customer:")
cus.print_items()
print("Export Customer to JSON FILE:")
cus.export_json("../datasets/customers.json")