from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.CustomerInfoWindow import Ui_CustomerInfoWindow


class CustomerInfoWindowEx(Ui_CustomerInfoWindow):
    def __init__(self, login_window_ex):
        self.login_window_ex = login_window_ex
        self.file_customers  = "datasets/customers.json"

    def setupUi(self, Window):
        super().setupUi(Window)
        self.Window = Window
        self.btnContinue.clicked.connect(self.process_continue)
        self.btnCancel.clicked.connect(self.Window.close)

    def showWindow(self):
        self.Window.show()

    def _lookup_cus_type(self, phone: str) -> str:
        """Tra cứu customers.json theo SĐT.
        Trả về 'VIP' nếu tìm thấy và type là VIP, ngược lại 'Normal'."""
        if not phone:
            return "Normal"
        try:
            from models.customers import Customers
            lc = Customers()
            lc.import_json(self.file_customers)
            existing = lc.find_by_phone(phone)
            if existing:
                return existing.cus_type
        except Exception:
            pass
        return "Normal"

    def process_continue(self):
        name  = self.lineEditName.text().strip()
        phone = self.lineEditPhone.text().strip()

        # Tự động xác định VIP/Normal từ JSON — khách không tự chọn
        cus_type = self._lookup_cus_type(phone)

        cus_info = {
            "name":     name if name else "Guest",
            "phone":    phone,
            "cus_type": cus_type
        }

        from ui.MainWindowEx import MainWindowEx
        self.main_win = QMainWindow()
        self.main_ex  = MainWindowEx(cus_info, self.login_window_ex)
        self.main_ex.setupUi(self.main_win)
        self.main_ex.showWindow()
        self.Window.close()
