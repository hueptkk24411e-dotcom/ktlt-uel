import json

from models.customer import Customer
from models.mycollections import MyCollections

class Customers(MyCollections):
    def import_json(self, filename):
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data['customers']:
                it = Customer(p['CustomerUserName'], p['PhoneNumber'],p['Type'],p['Rating'])
                self.add_item(it)

    def export_json(self, filename):
        data = {'customers': []}
        for it in self.list:
            data['customers'].append({
                'CustomerUserName': it.CustomerUserName,
                'PhoneNumber': it.PhoneNumber,
                'Type': it.Type,
                'Rating': it.Rating
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def login(self, uid):
        for item in self.list:
            if item.CustomerUserName == uid:
                return item
        return None