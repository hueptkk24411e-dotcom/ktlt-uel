"""
PaymentWindowEx.py
──────────────────
CẬP NHẬT SO VỚI FILE GỐC:
  • Dùng Ui_PaymentWindow MỚI (PaymentWindow.py vừa tạo) thay vì file cũ.
  • Thêm logic chọn phương thức thanh toán:
      - radioQR   → ẩn lblCashInfo, hiện labelQR với ảnh QR
      - radioCash → ẩn labelQR, hiện lblCashInfo
  • Load ảnh QR từ thư mục images/ (đặt file qr.png hoặc qr.jpg vào đó).
  • Khi nhấn DONE → mở FeedbackWindow (giống gốc).
"""

import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap

from nail_shop.nail_shop.ui.PaymentWindow import Ui_PaymentWindow

QR_IMAGE_NAMES = ("qr.png", "qr.jpg", "download.png")   # thử lần lượt


class PaymentWindowEx(Ui_PaymentWindow):
    def __init__(self, cus_info, subtotal, discount, total,
                 technician, login_window_ex, main_window):
        self.cus_info        = cus_info
        self.subtotal        = subtotal
        self.discount        = discount
        self.total           = total
        self.technician      = technician
        self.login_window_ex = login_window_ex
        self.main_window     = main_window
        self.is_vip          = (cus_info.get("cus_type", "Normal") == "VIP")

    def setupUi(self, Window):
        super().setupUi(Window)
        self.Window = Window

        # ── Hiện tổng tiền ────────────────────────────────────────
        self.lblTotalValue.setText(f"${self.total:.2f}")

        # ── Load ảnh QR ───────────────────────────────────────────
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir  = os.path.join(base_dir, "..", "images")
        qr_path  = None
        for name in QR_IMAGE_NAMES:
            candidate = os.path.join(img_dir, name)
            if os.path.exists(candidate):
                qr_path = candidate
                break

        if qr_path:
            self.labelQR.setPixmap(QPixmap(qr_path))
            self.labelQR.setText("")
        else:
            self.labelQR.setText("📱 QR not found\nPlace qr.png in images/")

        # ── Radio button logic ────────────────────────────────────
        self.radioQR.toggled.connect(self._on_payment_method_changed)
        self.radioCash.toggled.connect(self._on_payment_method_changed)
        # Khởi tạo trạng thái ban đầu
        self._on_payment_method_changed()

        # ── Confirm ───────────────────────────────────────────────
        self.btnConfirm.clicked.connect(self.process_confirm)

    def showWindow(self):
        self.Window.show()

    def _on_payment_method_changed(self):
        """Ẩn/hiện QR hoặc thông báo tiền mặt tuỳ lựa chọn."""
        if self.radioQR.isChecked():
            self.labelQR.setVisible(True)
            self.lblCashInfo.setVisible(False)
        else:
            self.labelQR.setVisible(False)
            self.lblCashInfo.setVisible(True)

    def process_confirm(self):
        method = "QR / Bank Transfer" if self.radioQR.isChecked() else "Cash"
        name   = self.cus_info.get("name", "Guest")

        QMessageBox.information(
            self.Window, "Payment Successful",
            f"Thank you, {name}!\n\n"
            f"Total paid : ${self.total:.2f}\n"
            f"Method     : {method}\n"
            f"Technician : {self.technician}\n\n"
            "We hope to see you again! 💅"
        )
        self.Window.close()
        self._open_feedback()

    def _open_feedback(self):
        from ui.FeedbackWindowEx import FeedbackWindowEx
        self._fb_win = QMainWindow()
        self._fb_ex  = FeedbackWindowEx(
            cus_info=self.cus_info,
            login_window_ex=self.login_window_ex,
            emenu_window=self.main_window
        )
        self._fb_ex.setupUi(self._fb_win)
        self._fb_ex.showWindow()
