import json
from models.order import Order


class Orders:
    def __init__(self):
        self.list = []
        self.filename = None

    def add_item(self, item):
        self.list.append(item)

    def print_items(self):
        for it in self.list:
            print(it)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()
        try:
            with open(filename, encoding='utf-8') as f:
                data = json.load(f)
                for p in data.get('orders', []):
                    it = Order(
                        order_id   = p.get('order_id'),
                        cus_name   = p.get('cus_name'),
                        cus_phone  = p.get('cus_phone'),
                        items      = p.get('items', []),
                        subtotal   = p.get('subtotal', 0.0),
                        discount   = p.get('discount', 0.0),
                        total      = p.get('total', 0.0),
                        technician = p.get('technician'),
                        method     = p.get('method'),
                        date       = p.get('date'),
                    )
                    self.add_item(it)
        except (FileNotFoundError, json.JSONDecodeError):
            # File chưa có hoặc rỗng → bắt đầu với list trống
            self.list = []

    def export_json(self, filename=None):
        if filename:
            self.filename = filename
        data = {'orders': []}
        for it in self.list:
            data['orders'].append({
                'order_id':   it.order_id,
                'cus_name':   it.cus_name,
                'cus_phone':  it.cus_phone,
                'items':      it.items,
                'subtotal':   it.subtotal,
                'discount':   it.discount,
                'total':      it.total,
                'technician': it.technician,
                'method':     it.method,
                'date':       it.date,
            })
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def find_item(self, order_id):
        for it in self.list:
            if it.order_id == order_id:
                return it
        return None

    def generate_id(self):
        """Tự sinh order_id tiếp theo dựa trên số lượng hiện có."""
        return f"ORD{len(self.list) + 1:04d}"
