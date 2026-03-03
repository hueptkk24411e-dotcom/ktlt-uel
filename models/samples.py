import json
from models.sample import Sample

class Samples:
    def __init__(self):
        self.list=[]
    def add_item(self,item):
        self.list.append(item)
    def print_items(self):
        for it in self.list:
            print(it)

    def import_json(self,filename):
         self.filename=filename
         self.list.clear()
         with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for p in data['samples']:
                it=Sample(p['SampleID'],p['SampleName'],p['SamplePrice'],p["SampleQuantity"])
                self.add_item(it)

    def export_json(self,filename):
        self.filename = filename
        data = {'samples': []}
        for it in self.list:
            data['samples'].append({
                'SampleID': it.SampleID,
                'SampleName': it.SampleName,
                'SamplePrice': it.SamplePrice,
                'SampleQuantity':it.SampleQuantity
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def find_item(self,SampleID):
        result=None#giả sử not found
        for it in self.list:
            if it.SampleID==SampleID:
                result=it#FOUND
                break
        return result

    def find_item(self, SampleID):
        result = None  # giả sử not found
        for it in self.list:
            if it.SampleID == SampleID:
                result = it  # FOUND
                break
        return result

    def remove_item(self, SampleID):
        result = self.find_item(SampleID)
        if result != None:
            self.list.remove(result)
            # write dataset into file
            self.export_json(self.filename)

    def update_item(self, it):
        exist_it = self.find_item(it.id)
        if exist_it == None:
            # NOT FOUND--> insert a new one
            self.add_item(exist_it)
            # write dataset into file
            self.export_json(self.filename)
            return True
        else:
            # updating value at the MEMORY
            exist_it.SampleID = it.SampleID
            exist_it.SampleName = it.SampleName
            exist_it.SamplePrice = it.SamplePrice
            exist_it.SampleQuantity = it.SampleQuantity
            # write dataset into file
            self.export_json(self.filename)
            return True  # update successful