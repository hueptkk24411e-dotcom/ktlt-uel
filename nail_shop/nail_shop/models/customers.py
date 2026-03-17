import json

from nail_shop.nail_shop.models.customer import Customer


class Customers:
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
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
            for p in data['customers']:
                it = Customer(p['name'], p['phone'], p['cus_type'], p.get('rating', 0))
                self.add_item(it)

    def export_json(self, filename=None):
        if filename:
            self.filename = filename
        data = {'customers': []}
        for it in self.list:
            data['customers'].append({
                'name': it.name,
                'phone': it.phone,
                'cus_type': it.cus_type,
                'rating': it.rating
            })
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def find_by_phone(self, phone):
        for it in self.list:
            if str(it.phone) == str(phone):
                return it
        return None

    def find_item(self, phone):
        return self.find_by_phone(phone)

    def remove_item(self, phone):
        result = self.find_by_phone(phone)
        if result:
            self.list.remove(result)
            self.export_json()
