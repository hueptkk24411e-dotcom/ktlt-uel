import json

from models.manager import Manager
from models.mycollections import MyCollections

class Managers(MyCollections):
    def import_json(self, filename):
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data['managers']:
                it = Manager(p['ManagerID'], p['ManagerName'], p['ManagerUsername'],p['ManagerPassword'])
                self.add_item(it)

    def export_json(self, filename):
        data = {'managers': []}
        for it in self.list:
            data['managers'].append({
                'ManagerID': it.ManagerID,
                'ManagerName': it.ManagerName,
                'ManagerUsername': it.ManagerUsername,
                'ManagerPassword': it.ManagerPassword
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

