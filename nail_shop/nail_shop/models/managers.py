import json

from nail_shop.nail_shop.models.manager import Manager


class Managers:
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
            for p in data['managers']:
                it = Manager(p['manager_id'], p['name'], p['username'], p['password'])
                self.add_item(it)

    def export_json(self, filename=None):
        if filename:
            self.filename = filename
        data = {'managers': []}
        for it in self.list:
            data['managers'].append({
                'manager_id': it.manager_id,
                'name': it.name,
                'username': it.username,
                'password': it.password
            })
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def find_by_username(self, username):
        for it in self.list:
            if it.username.strip().lower() == username.strip().lower():
                return it
        return None
