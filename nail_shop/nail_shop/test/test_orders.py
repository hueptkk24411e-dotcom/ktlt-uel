import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.order import Order
from models.orders import Orders

# 4 orders test các trường hợp khác nhau:
#   ORD0001 — VIP, nhiều món, QR
#   ORD0002 — Normal, 1 món, Cash
#   ORD0003 — Guest (không SĐT), Custom nail → "Other" trong chart
#   ORD0004 — VIP, mix 2 mùa khác nhau trong 1 order

orders = [
    Order(
        order_id   = "ORD0001",
        cus_name   = "Nguyen An",
        cus_phone  = "0901111111",
        items      = ["White Flora Charm x1 ($36.00)", "Pink Crystal Fairy x1 ($40.00)"],
        subtotal   = 76.0,
        discount   = 15.2,
        total      = 60.8,
        technician = "Emily",
        method     = "QR / Bank Transfer",
        date       = "2026-03-01 10:00",
    ),
    Order(
        order_id   = "ORD0002",
        cus_name   = "Tran Binh",
        cus_phone  = "0902222222",
        items      = ["Winter Snowman x1 ($30.00)"],
        subtotal   = 30.0,
        discount   = 0.0,
        total      = 30.0,
        technician = "Sophie",
        method     = "Cash",
        date       = "2026-03-02 14:00",
    ),
    Order(
        order_id   = "ORD0003",
        cus_name   = "Guest",
        cus_phone  = "",
        items      = ["Custom: French, Short, Pink x1 ($50.00)"],
        subtotal   = 50.0,
        discount   = 0.0,
        total      = 50.0,
        technician = "Any available",
        method     = "Cash",
        date       = "2026-03-03 09:30",
    ),
    Order(
        order_id   = "ORD0004",
        cus_name   = "Pham Duc",
        cus_phone  = "0904444444",
        items      = ["Green Matcha Muse x1 ($36.00)", "Ocean Pearl Dream x1 ($40.00)"],
        subtotal   = 76.0,
        discount   = 15.2,
        total      = 60.8,
        technician = "Emily",
        method     = "QR / Bank Transfer",
        date       = "2026-03-04 16:00",
    ),
]

lo = Orders()
for o in orders:
    lo.add_item(o)

os.makedirs("../datasets", exist_ok=True)
lo.export_json("../datasets/orders.json")
lo.print_items()
print(f"Done: orders.json — {len(orders)} orders")
