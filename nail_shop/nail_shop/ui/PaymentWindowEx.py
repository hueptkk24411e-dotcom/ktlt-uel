"""
PaymentWindowEx.py
──────────────────
THAY ĐỔI SO VỚI FILE GỐC:
  [1] __init__() nhận thêm tham số cart (list các tuple (name, price, qty))
      → dùng để ghi chi tiết order vào orders.json

  [2] process_confirm() gọi thêm _save_order() trước khi mở FeedbackWindow
      → toàn bộ logic hiển thị QMessageBox và mở Feedback giữ nguyên

  [3] Thêm method _save_order() hoàn toàn mới
      → tạo Order object, ghi vào datasets/orders.json
      → nếu file chưa có hoặc lỗi thì bỏ qua, không crash app
"""

import os
import datetime
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap

from ui.PaymentWindow import Ui_PaymentWindow


QR_IMAGE_NAMES = ("qr.png", "qr.jpg", "download.png")


class PaymentWindowEx(Ui_PaymentWindow):
    # ── [1] THAY ĐỔI: thêm tham số cart ────────────────────────────────────────
    # cart là self.cart từ MainWindowEx, dạng list of tuple: (name, price, qty)
    def __init__(self, cus_info, subtotal, discount, total,
                 technician, login_window_ex, main_window, cart=None):
        self.cus_info        = cus_info
        self.subtotal        = subtotal
        self.discount        = discount
        self.total           = total
        self.technician      = technician
        self.login_window_ex = login_window_ex
        self.main_window     = main_window
        self.is_vip          = (cus_info.get("cus_type", "Normal") == "VIP")
        self.cart            = cart or []            # [1] THÊM MỚI
    # ── hết thay đổi [1] ────────────────────────────────────────────────────────

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
        self._on_payment_method_changed()

        # ── Confirm ───────────────────────────────────────────────
        self.btnConfirm.clicked.connect(self.process_confirm)

    def showWindow(self):
        self.Window.show()

    def _on_payment_method_changed(self):
        if self.radioQR.isChecked():
            self.labelQR.setVisible(True)
            self.lblCashInfo.setVisible(False)
        else:
            self.labelQR.setVisible(False)
            self.lblCashInfo.setVisible(True)

    # ── [2] THAY ĐỔI: gọi thêm _save_order() trước khi mở Feedback ─────────────
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

        self._save_order(method)                     # [2] THÊM MỚI — lưu order
        self.Window.close()
        self._open_feedback()
    # ── hết thay đổi [2] ────────────────────────────────────────────────────────

    # ── [3] METHOD MỚI HOÀN TOÀN ────────────────────────────────────────────────
    def _save_order(self, method: str):
        """Tạo Order object từ thông tin hiện có và ghi vào datasets/orders.json.
        Bắt toàn bộ exception để đảm bảo nếu lỗi thì app không crash."""
        try:
            from models.orders import Orders
            from models.order import Order

            file_orders = "datasets/orders.json"
            lo = Orders()
            lo.import_json(file_orders)

            # Chuyển cart [(name, price, qty), ...] → list string dễ đọc
            # vd: ["White Flora Charm x2 ($72.00)", "Custom: French, Short x1 ($50.00)"]
            items_str = [
                f"{name} x{qty} (${price * qty:.2f})"
                for name, price, qty in self.cart
            ]

            new_order = Order(
                order_id   = lo.generate_id(),
                cus_name   = self.cus_info.get("name", "Guest"),
                cus_phone  = self.cus_info.get("phone", ""),
                items      = items_str,
                subtotal   = round(self.subtotal, 2),
                discount   = round(self.discount, 2),
                total      = round(self.total, 2),
                technician = self.technician,
                method     = method,
                date       = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            )

            lo.add_item(new_order)
            lo.export_json(file_orders)

        except Exception as e:
            # Không báo lỗi ra màn hình khách — chỉ in console để debug
            print(f"[PaymentWindowEx] _save_order failed: {e}")
    # ── hết thay đổi [3] ────────────────────────────────────────────────────────

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
