import json

from nail_shop.nail_shop.models.sample import Sample


class Samples:
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
            for p in data['samples']:
                it = Sample(p['sample_id'], p['name'], p['price'],
                            p.get('season', ''))
                self.add_item(it)

    def export_json(self, filename=None):
        if filename:
            self.filename = filename
        data = {'samples': []}
        for it in self.list:
            data['samples'].append({
                'sample_id': it.sample_id,
                'name': it.name,
                'price': it.price,
                'season': it.season
            })
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def find_item(self, sample_id):
        for it in self.list:
            if it.sample_id == sample_id:
                return it
        return None

    def find_by_season(self, season):
        return [it for it in self.list if it.season.lower() == season.lower()]

    def remove_item(self, sample_id):
        result = self.find_item(sample_id)
        if result:
            self.list.remove(result)
            self.export_json()

    def update_item(self, updated):
        exist = self.find_item(updated.sample_id)
        if exist:
            exist.name = updated.name
            exist.price = updated.price
            exist.season = updated.season
            self.export_json()
            return True
        return False
