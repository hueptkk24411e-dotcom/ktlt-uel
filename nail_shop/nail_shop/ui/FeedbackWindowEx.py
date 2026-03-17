"""
FeedbackWindowEx.py
────────────────────
Import từ ui.constants — KHÔNG import trực tiếp từ FeedbackWindow.py.
Sửa lỗi: self.starBtns không tồn tại trong Ui_RatingUI,
          nay tự build từ STAR_BTN_NAMES trong constants.py.
"""
from PyQt6.QtWidgets import QWidget, QMessageBox

from nail_shop.nail_shop.models.customer import Customer
from nail_shop.nail_shop.models.customers import Customers
from nail_shop.nail_shop.ui.FeedbackWindow import Ui_RatingUI
from nail_shop.nail_shop.ui.constants import STAR_BTN_NAMES, STAR_ON, STAR_OFF, RATING_LABELS


class FeedbackWindowEx(Ui_RatingUI):
    def __init__(self, cus_info, login_window_ex, emenu_window):
        self.cus_info        = cus_info
        self.login_window_ex = login_window_ex
        self.emenu_window    = emenu_window
        self.selected_stars  = 0
        self.file_customers  = "datasets/customers.json"
        self._star_btns      = []

    def setupUi(self, Window):
        self.Window = Window

        # Ui_RatingUI là QWidget-based → bọc vào centralwidget của QMainWindow
        self._ui_widget = QWidget()
        super().setupUi(self._ui_widget)
        Window.setCentralWidget(self._ui_widget)
        Window.setWindowTitle("Rate Our Service")
        Window.resize(450, 460)

        # Build list nút sao từ tên object đã định nghĩa trong constants
        self._star_btns = [
            getattr(self, name)
            for name in STAR_BTN_NAMES
            if hasattr(self, name)
        ]

        # Connect từng nút sao
        for idx, btn in enumerate(self._star_btns, start=1):
            btn.clicked.connect(lambda _, i=idx: self._on_star_click(i))

        self.btnSubmit.clicked.connect(self._submit)

    def showWindow(self):
        self.Window.show()

    def _on_star_click(self, star_index: int):
        self.selected_stars = star_index
        for i, btn in enumerate(self._star_btns, start=1):
            btn.setStyleSheet(STAR_ON if i <= star_index else STAR_OFF)
        self.lblInstruction.setText(RATING_LABELS.get(star_index, ""))

    def _submit(self):
        if self.selected_stars == 0:
            QMessageBox.warning(self.Window, "Notice",
                                "Please select a star rating first.")
            return

        feedback_text = self.lineEditFeedback.text().strip()

        lc = Customers()
        lc.import_json(self.file_customers)
        phone = self.cus_info.get("phone", "")
        name  = self.cus_info.get("name", "Guest")
        ctype = self.cus_info.get("cus_type", "Normal")

        if phone:
            existing = lc.find_by_phone(phone)
            if existing:
                existing.rating = self.selected_stars
                if hasattr(existing, "feedback"):
                    existing.feedback = feedback_text
            else:
                c = Customer(name, phone, ctype, self.selected_stars)
                if hasattr(c, "feedback"):
                    c.feedback = feedback_text
                lc.add_item(c)
        elif name != "Guest":
            c = Customer(name, "", ctype, self.selected_stars)
            if hasattr(c, "feedback"):
                c.feedback = feedback_text
            lc.add_item(c)

        lc.export_json(self.file_customers)

        msg = f"Thank you for your {self.selected_stars}★ rating!"
        if feedback_text:
            msg += f"\n\nYour feedback: \"{feedback_text}\""
        msg += "\n\nWe look forward to serving you again. 💅"

        QMessageBox.information(self.Window, "Thank You!", msg)
        self._finish()

    def _finish(self):
        self.Window.close()
        if self.emenu_window:
            self.emenu_window.close()
        if self.login_window_ex:
            self.login_window_ex.LoginWindow.show()
