"""
MainWindowEx.py
───────────────
THAY ĐỔI SO VỚI FILE GỐC:
  [1] _open_payment() truyền thêm tham số cart=self.cart sang PaymentWindowEx
      → PaymentWindowEx cần tham số này để lưu chi tiết order vào orders.json
      → Không thay đổi gì logic hiển thị hay tính tiền, chỉ thêm 1 dòng truyền tham số
"""
import os
from PyQt6.QtWidgets import (
    QTableWidgetItem, QMessageBox, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QMainWindow, QDialog, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

from models.samples import Samples
from models.employees import Employees
from ui.MainWindow import Ui_MainWindow
from ui.constants import STYLE_ACTION_BTN, STYLE_PRODUCT_BTN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR  = os.path.join(BASE_DIR, "..", "images")
VIP_DISCOUNT = 0.20

# ── Card styles ───────────────────────────────────────────────────
STYLE_CARD = """
    QWidget#card {
        background-color: white;
        border: 2px solid rgb(200, 225, 248);
        border-radius: 16px;
    }
    QWidget#card:hover {
        border: 2px solid rgb(67, 139, 196);
        background-color: rgb(240, 248, 255);
    }
"""

STYLE_SELECT_BTN = """
    QPushButton {
        background-color: rgb(167, 212, 238);
        color: rgb(0, 0, 127);
        border: 2px solid rgb(67, 139, 196);
        border-radius: 14px;
        font-size: 12px;
        font-weight: bold;
        font-family: "Georgia";
        padding: 6px 10px;
    }
    QPushButton:hover  { background-color: #A6C8FF; border: 2px solid #7FAFFF; color: white; }
    QPushButton:pressed{ background-color: #7FAFFF; border: 2px solid #4A90E2; }
"""

# Badge màu riêng cho từng mùa
SEASON_BADGE = {
    "Spring": ("🌸 Spring", "#fde8f0", "#b5376a"),
    "Summer": ("☀️ Summer", "#fff3cc", "#8a6200"),
    "Autumn": ("🍂 Autumn", "#ffeadb", "#9c4400"),
    "Winter": ("❄️ Winter", "#dff0ff", "#0a5a8a"),
}


class ProductCard(QWidget):
    _COLOR_NORMAL = (200, 225, 248)
    _COLOR_HOVER  = (67,  139, 196)
    _RADIUS       = 16

    def __init__(self, sample, on_add_callback):
        super().__init__()
        self.setObjectName("card")
        self._hovered = False
        self.setFixedSize(190, 320)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setStyleSheet(
            "QWidget#card { background-color: white; border-radius: 16px; }"
        )

        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 10)
        lay.setSpacing(5)

        img_wrap = QWidget()
        img_wrap.setFixedSize(174, 190)
        img_wrap.setStyleSheet("background: transparent;")

        lbl_img = QLabel(img_wrap)
        lbl_img.setGeometry(0, 0, 174, 190)
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_img.setStyleSheet(
            "background-color: rgb(234, 242, 251);"
            "border-radius: 10px;"
            "border: none;"
        )

        slug     = sample.name.lower().replace(" ", "_")
        img_path = os.path.join(IMG_DIR, f"{slug}.jpg")
        if not os.path.exists(img_path):
            img_path = os.path.join(IMG_DIR, f"{slug}.png")
        if os.path.exists(img_path):
            pix = QPixmap(img_path).scaled(
                174, 190,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            lbl_img.setPixmap(pix)
            lbl_img.setScaledContents(True)
        else:
            lbl_img.setText("💅")
            lbl_img.setFont(QFont("Arial", 32))

        season = sample.season or ""
        badge_txt, badge_bg, badge_fg = SEASON_BADGE.get(
            season, (season, "#e8f4fb", "#2c7db5")
        )
        lbl_badge = QLabel(badge_txt, img_wrap)
        lbl_badge.setStyleSheet(
            f"background-color: {badge_bg};"
            f"color: {badge_fg};"
            "border-radius: 9px;"
            "font-size: 10px;"
            "font-weight: bold;"
            "padding: 3px 7px;"
            "border: none;"
        )
        lbl_badge.adjustSize()
        lbl_badge.move(6, 6)
        lbl_badge.raise_()

        lay.addWidget(img_wrap)

        lbl_name = QLabel(sample.name)
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setWordWrap(True)
        lbl_name.setFixedHeight(34)
        lbl_name.setStyleSheet(
            "color: rgb(0, 0, 127);"
            "font-size: 12px;"
            "font-weight: bold;"
            "border: none;"
            "background: transparent;"
        )
        lay.addWidget(lbl_name)

        lbl_price = QLabel(f"${int(sample.price)}")
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_price.setFixedHeight(24)
        lbl_price.setStyleSheet(
            "color: #438bc4;"
            "font-size: 16px;"
            "font-weight: bold;"
            "border: none;"
            "background: transparent;"
        )
        lay.addWidget(lbl_price)

        btn_add = QPushButton("Select Design")
        btn_add.setFixedHeight(32)
        btn_add.setStyleSheet(STYLE_SELECT_BTN)
        btn_add.setCursor(Qt.CursorShape.OpenHandCursor)
        btn_add.clicked.connect(
            lambda _, n=sample.name, p=sample.price: on_add_callback(n, p)
        )
        lay.addWidget(btn_add)

    def event(self, e):
        from PyQt6.QtCore import QEvent
        from PyQt6.QtGui import QPainter, QPen, QColor
        if e.type() == QEvent.Type.HoverEnter:
            self._hovered = True; self.update()
        elif e.type() == QEvent.Type.HoverLeave:
            self._hovered = False; self.update()
        return super().event(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        from PyQt6.QtGui import QPainter, QPen, QColor
        from PyQt6.QtCore import QRect
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r, g, b = self._COLOR_HOVER if self._hovered else self._COLOR_NORMAL
        pen = QPen(QColor(r, g, b)); pen.setWidth(2); p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(1, 1, self.width()-2, self.height()-2, self._RADIUS, self._RADIUS)


class TechnicianDialog(QMainWindow):
    def __init__(self, employees_list, on_select_callback):
        super().__init__()
        from PyQt6.QtWidgets import QTableWidget
        self.setWindowTitle("Select Technician")
        self.setFixedSize(380, 300)
        central = QWidget(); lay = QVBoxLayout(central)
        lay.setContentsMargins(16,16,16,16); lay.setSpacing(10)
        lbl = QLabel("Double-click to select a technician:")
        lbl.setStyleSheet("font-size:13px;font-weight:bold;color:rgb(0,0,127);")
        lay.addWidget(lbl)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID","Name","Experience"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("QTableWidget{background:white;border:2px solid rgb(170,210,250);border-radius:8px;}"
            "QHeaderView::section{background:rgb(167,212,238);color:rgb(0,0,127);font-weight:bold;padding:4px;border:none;}")
        self.table.setRowCount(len(employees_list))
        for r, emp in enumerate(employees_list):
            self.table.setItem(r, 0, QTableWidgetItem(emp.emp_id))
            self.table.setItem(r, 1, QTableWidgetItem(emp.name))
            self.table.setItem(r, 2, QTableWidgetItem(f"{emp.experience} yrs"))
        lay.addWidget(self.table)
        self.table.cellDoubleClicked.connect(
            lambda row, _: self._on_select(row, employees_list, on_select_callback))
        self.setCentralWidget(central)

    def _on_select(self, row, employees_list, callback):
        callback(employees_list[row].name); self.close()


class AboutUsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About My Nail Shop 💅"); self.setFixedSize(480, 400)
        self.setStyleSheet("background-color: rgb(234,242,251);")
        lay = QVBoxLayout(self); lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(14)
        hdr = QWidget(); hdr.setFixedHeight(64)
        hdr.setStyleSheet("background-color: rgb(167,212,238); border-radius: 14px;")
        hl = QVBoxLayout(hdr); hl.setContentsMargins(0, 6, 0, 6)
        lh = QLabel("MY NAIL SHOP"); lh.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lh.setStyleSheet("font-size:22px;font-weight:bold;font-family:Georgia,serif;color:white;")
        ls = QLabel("Where Your Beauty and Satisfaction Come First")
        ls.setAlignment(Qt.AlignmentFlag.AlignCenter); ls.setStyleSheet("font-size:11px;color:white;")
        hl.addWidget(lh); hl.addWidget(ls); lay.addWidget(hdr)
        box = QFrame()
        box.setStyleSheet("QFrame{background-color:white;border:2px solid rgb(170,210,250);border-radius:12px;}")
        bl = QVBoxLayout(box); bl.setContentsMargins(20, 16, 20, 16); bl.setSpacing(10)
        for icon, text in [("💅","Professional nail care since 2018"),("📍","123 Beauty Street, Ho Chi Minh City"),
            ("📞","Hotline: 0909 123 456"),("🕐","Open daily: 9:00 AM – 8:00 PM"),
            ("⭐","Specialties: Gel nails, nail art, custom designs"),("💬",'"Beauty is not just a look — it\'s a feeling."')]:
            rw = QWidget(); rl = QHBoxLayout(rw); rl.setContentsMargins(0,0,0,0); rl.setSpacing(10)
            li = QLabel(icon); li.setFixedWidth(24); li.setStyleSheet("font-size:16px;")
            lt = QLabel(text); lt.setStyleSheet("color:rgb(0,0,127);font-size:13px;"); lt.setWordWrap(True)
            rl.addWidget(li); rl.addWidget(lt, stretch=1); bl.addWidget(rw)
        lay.addWidget(box)
        bc = QPushButton("Close"); bc.setFixedHeight(36); bc.setStyleSheet(STYLE_ACTION_BTN)
        bc.clicked.connect(self.accept); lay.addWidget(bc)


class MainWindowEx(Ui_MainWindow):
    def __init__(self, cus_info: dict, login_window_ex):
        self.cus_info = cus_info; self.login_window_ex = login_window_ex
        self.is_vip = (cus_info.get("cus_type", "Normal") == "VIP")
        self.file_samples = "datasets/samples.json"; self.file_employees = "datasets/employees.json"
        self.lp = Samples(); self.le = Employees()
        self.lp.import_json(self.file_samples); self.le.import_json(self.file_employees)
        self.cart = []; self.subtotal = 0.0
        self.selected_technician = None; self.current_season = "All"
        self._tech_win = None; self._custom_win = None; self._custom_wex = None
        self._payment_win = None; self._about_dlg = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow); self.MainWindow = MainWindow
        name = self.cus_info.get("name", "Guest")
        badge = f"👤 {name}" + ("  |  ⭐ VIP — 20% OFF" if self.is_vip else "")
        self.lblCustomerBadge.setText(badge)
        self.discountRow.setVisible(self.is_vip)
        self.btnAll.clicked.connect(lambda: self._switch_season("All"))
        self.btnSpring.clicked.connect(lambda: self._switch_season("Spring"))
        self.btnSummer.clicked.connect(lambda: self._switch_season("Summer"))
        self.btnAutumn.clicked.connect(lambda: self._switch_season("Autumn"))
        self.btnWinter.clicked.connect(lambda: self._switch_season("Winter"))
        self.btnCustomNail.clicked.connect(self._open_custom)
        self.actionSpring.triggered.connect(lambda: self._switch_season("Spring"))
        self.actionSummer.triggered.connect(lambda: self._switch_season("Summer"))
        self.actionAutumn.triggered.connect(lambda: self._switch_season("Autumn"))
        self.actionWinter.triggered.connect(lambda: self._switch_season("Winter"))
        self.actionAboutUs.triggered.connect(self._open_about_us)
        self.btnRemove.clicked.connect(self._remove_from_cart)
        self.btnClearCart.clicked.connect(self._clear_cart)
        self.btnPickTech.clicked.connect(self._open_technician)
        self.btnCheckout.clicked.connect(self._open_payment)
        self.btnBackToLogin.clicked.connect(self._back_to_login)
        self._switch_season("All")

    def showWindow(self): self.MainWindow.show()

    def _open_about_us(self):
        self._about_dlg = AboutUsDialog(self.MainWindow); self._about_dlg.exec()

    def _switch_season(self, season):
        self.current_season = season
        for btn, s in [(self.btnAll,"All"),(self.btnSpring,"Spring"),(self.btnSummer,"Summer"),
                       (self.btnAutumn,"Autumn"),(self.btnWinter,"Winter")]:
            btn.setChecked(s == season)
        samples = self.lp.list if season == "All" else self.lp.find_by_season(season)
        self._populate_grid(samples)

    def _populate_grid(self, samples):
        while self.productGrid.count():
            item = self.productGrid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        cols = 5
        for idx, sample in enumerate(samples):
            self.productGrid.addWidget(ProductCard(sample, self.add_to_cart), idx//cols, idx%cols)
        rem = len(samples) % cols
        if rem:
            for i in range(cols - rem):
                sp = QWidget(); sp.setFixedSize(190, 320)
                self.productGrid.addWidget(sp, len(samples)//cols, rem+i)

    def add_to_cart(self, item_name, unit_price):
        for i, (name, price, qty) in enumerate(self.cart):
            if name == item_name:
                self.cart[i] = (name, price, qty+1); self._refresh_cart(); return
        self.cart.append((item_name, unit_price, 1)); self._refresh_cart()

    def _refresh_cart(self):
        self.tableCart.setRowCount(0); self.subtotal = 0.0
        for name, price, qty in self.cart:
            row = self.tableCart.rowCount(); self.tableCart.insertRow(row)
            in_ = QTableWidgetItem(name)
            iq  = QTableWidgetItem(str(qty))
            iu  = QTableWidgetItem(f"${price:.2f}")
            it  = QTableWidgetItem(f"${price*qty:.2f}")
            iq.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            iu.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
            it.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
            self.tableCart.setItem(row,0,in_); self.tableCart.setItem(row,1,iq)
            self.tableCart.setItem(row,2,iu);  self.tableCart.setItem(row,3,it)
            self.subtotal += price*qty
        discount = self.subtotal*VIP_DISCOUNT if self.is_vip else 0.0
        total = self.subtotal - discount
        self.lineEditSubtotal.setText(f"{self.subtotal:.2f} $")
        if self.is_vip: self.lineEditDiscount.setText(f"– {discount:.2f} $")
        self.lineEditTotal.setText(f"{total:.2f} $")

    def _remove_from_cart(self):
        row = self.tableCart.currentRow()
        if row < 0: QMessageBox.warning(self.MainWindow,"Warning","Please select an item to remove."); return
        del self.cart[row]; self._refresh_cart()

    def _clear_cart(self):
        if not self.cart: return
        if QMessageBox.question(self.MainWindow,"Clear Cart","Remove all items from cart?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.cart.clear(); self._refresh_cart()

    def _open_technician(self):
        self._tech_win = TechnicianDialog(self.le.list, self._set_technician); self._tech_win.show()

    def _set_technician(self, name):
        self.selected_technician = name
        self.lblTechnician.setText(f"✔  {name}")
        self.lblTechnician.setStyleSheet("color:rgb(0,100,0);font-weight:bold;font-size:12px;")

    def _open_custom(self):
        from ui.SelfCustomWindowEx import SelfCustomWindowEx
        self._custom_win = QMainWindow()
        self._custom_wex = SelfCustomWindowEx(self.add_to_cart)
        self._custom_wex.setupUi(self._custom_win)
        self._custom_wex.showWindow()

    # ── [1] THAY ĐỔI: truyền thêm cart=self.cart sang PaymentWindowEx ──────────
    # Trước đây chỉ truyền subtotal/discount/total.
    # Bây giờ truyền thêm self.cart để PaymentWindowEx biết khách order món gì,
    # dùng để ghi chi tiết vào orders.json sau khi thanh toán thành công.
    def _open_payment(self):
        if not self.cart: QMessageBox.warning(self.MainWindow,"Empty Cart","Please add items first."); return
        discount = self.subtotal*VIP_DISCOUNT if self.is_vip else 0.0
        total = self.subtotal - discount
        from ui.PaymentWindowEx import PaymentWindowEx
        self._payment_win = QMainWindow()
        self._payment_ex  = PaymentWindowEx(
            cus_info=self.cus_info, subtotal=self.subtotal,
            discount=discount, total=total,
            technician=self.selected_technician or "Any available",
            cart=self.cart,                          # [1] THÊM MỚI
            login_window_ex=self.login_window_ex, main_window=self.MainWindow)
        self._payment_ex.setupUi(self._payment_win); self._payment_ex.showWindow()
    # ── hết thay đổi [1] ────────────────────────────────────────────────────────

    def _back_to_login(self):
        self.login_window_ex.LoginWindow.show(); self.MainWindow.close()
