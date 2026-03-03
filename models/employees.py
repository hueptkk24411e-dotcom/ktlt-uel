import json

from models.employee import Employee
from models.mycollections import MyCollections

class Employees(MyCollections):
    def import_json(self, filename):
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data['employees']:
                it = Employee(p['EmployeeId'], p['EmployeeName'], p['Experience'],p['CustomerBooked'])
                self.add_item(it)

    def export_json(self, filename):
        data = {'employees': []}
        for it in self.list:
            data['employees'].append({
                'EmployeeId': it.EmployeeId,
                'EmployeeName': it.EmployeeName,
                'Experience': it.Experience,
                'CustomerBooked': it.CustomerBooked
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

