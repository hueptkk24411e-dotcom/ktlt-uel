import json
from models.employee import Employee


class Employees:
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
            for p in data['employees']:
                it = Employee(p['emp_id'], p['name'], p['experience'])
                self.add_item(it)

    def export_json(self, filename=None):
        if filename:
            self.filename = filename
        data = {'employees': []}
        for it in self.list:
            data['employees'].append({
                'emp_id': it.emp_id,
                'name': it.name,
                'experience': it.experience
            })
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def find_item(self, emp_id):
        for it in self.list:
            if it.emp_id == emp_id:
                return it
        return None

    def remove_item(self, emp_id):
        result = self.find_item(emp_id)
        if result:
            self.list.remove(result)
            self.export_json()
