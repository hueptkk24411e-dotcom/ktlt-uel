class Order:
    def __init__(self, order_id=None, cus_name=None, cus_phone=None,
                 items=None, subtotal=None, discount=None, total=None,
                 technician=None, method=None, date=None):
        self.order_id   = order_id    # "ORD0001", "ORD0002", ...
        self.cus_name   = cus_name    # tên khách
        self.cus_phone  = cus_phone   # SĐT (có thể rỗng nếu là Guest)
        self.items      = items or [] # list string, vd: ["White Flora Charm x1", ...]
        self.subtotal   = subtotal    # float
        self.discount   = discount    # float (0.0 nếu không VIP)
        self.total      = total       # float
        self.technician = technician  # tên kỹ thuật viên
        self.method     = method      # "QR / Bank Transfer" hoặc "Cash"
        self.date       = date        # string "2025-01-01 14:30"

    def __str__(self):
        return (f"{self.order_id}\t{self.cus_name}\t{self.cus_phone}\t"
                f"{self.total}\t{self.method}\t{self.date}")
