from models.manager import Manager
from models.managers import Managers

# 4 manager với động vật khác employee
m1 = Manager("M01", "Hổ", "ho", "111111")
m2 = Manager("M02", "Voi", "voi", "333333")
m3 = Manager("M03", "Thỏ Trắng", "tho", "345678")
m4 = Manager("M04", "Cáo Đỏ", "cao", "456789")
mgr = Managers()
mgr.add_items([m1, m2, m3, m4])
print("List of Managers:")
mgr.print_items()

print("Export Managers to JSON FILE:")
mgr.export_json("../datasets/managers.json")