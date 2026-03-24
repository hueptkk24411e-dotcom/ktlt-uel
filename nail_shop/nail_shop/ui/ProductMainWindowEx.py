

import os
import shutil
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QTableWidgetItem, QMessageBox, QVBoxLayout, QFileDialog,
    QWidget, QDialog, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget
)
from PyQt6.QtGui import QPixmap

from models.samples import Samples
from models.sample import Sample
from models.customers import Customers
from models.customer import Customer
from models.employees import Employees
from models.employee import Employee
from models.orders import Orders
from ui.ProductMainWindow import Ui_ProductMainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR  = os.path.join(BASE_DIR, "..", "images")


class ProductMainWindowEx(Ui_ProductMainWindow):
    def __init__(self, login_window_ex):
        self.login_window_ex  = login_window_ex
        self.file_samples     = "datasets/samples.json"
        self.file_customers   = "datasets/customers.json"
        self.file_employees   = "datasets/employees.json"
        self.file_orders      = "datasets/orders.json"

        self.ls = Samples()
        self.lc = Customers()
        self.le = Employees()
        self.lo = Orders()

        self.ls.import_json(self.file_samples)
        self.lc.import_json(self.file_customers)
        self.le.import_json(self.file_employees)
        self.lo.import_json(self.file_orders)

        self._current_fig = None

    def setupUi(self, Window):
        super().setupUi(Window)
        self.Window = Window
        self._display_all()
        self._connect_signals()

    def showWindow(self):
        self.Window.show()

    # ── Display ────────────────────────────────────────────────────

    def _display_all(self):
        self._display_samples(self.ls.list)
        self._display_customers(self.lc.list)
        self._display_employees(self.le.list)
        self._display_orders(self.lo.list)

    def _display_samples(self, lst):
        self.tableSamples.setRowCount(0)
        for s in lst:
            r = self.tableSamples.rowCount()
            self.tableSamples.insertRow(r)
            for c, val in enumerate([s.sample_id, s.name, str(s.price), s.season]):
                self.tableSamples.setItem(r, c, QTableWidgetItem(val))

    def _display_customers(self, lst):
        self.tableCustomers.setRowCount(0)
        for c in lst:
            r = self.tableCustomers.rowCount()
            self.tableCustomers.insertRow(r)
            for col, val in enumerate([c.name, c.phone,
                                        c.cus_type, str(c.rating or 0)]):
                self.tableCustomers.setItem(r, col, QTableWidgetItem(val))

    def _display_employees(self, lst):
        self.tableEmployees.setRowCount(0)
        for e in lst:
            r = self.tableEmployees.rowCount()
            self.tableEmployees.insertRow(r)
            for c, val in enumerate([e.emp_id, e.name, str(e.experience)]):
                self.tableEmployees.setItem(r, c, QTableWidgetItem(val))

    # ──  hiện danh sách orders ──────────────────────
    def _display_orders(self, lst):
        """Hiện danh sách orders vào tableOrders."""
        self.tableOrders.blockSignals(True)
        self.tableOrders.setRowCount(0)
        for o in lst:
            r = self.tableOrders.rowCount()
            self.tableOrders.insertRow(r)
            for col, val in enumerate([
                o.order_id,
                o.cus_name   or "",
                o.cus_phone  or "",
                f"${o.total:.2f}",
                o.method     or "",
                o.date       or "",
            ]):
                self.tableOrders.setItem(r, col, QTableWidgetItem(val))
        self.tableOrders.blockSignals(False)


    # ── Signals ────────────────────────────────────────────────────

    def _connect_signals(self):
        # Table row click → fill form
        self.tableSamples.itemSelectionChanged.connect(self._fill_sample_form)
        self.tableCustomers.itemSelectionChanged.connect(self._fill_customer_form)
        self.tableEmployees.itemSelectionChanged.connect(self._fill_employee_form)

        # Sample CRUD
        self.btnSampleSave.clicked.connect(self._save_sample)
        self.btnSampleRemove.clicked.connect(self._remove_sample)
        self.btnSampleSearch.clicked.connect(self._search_sample)
        self.btnSampleClear.clicked.connect(self._clear_sample_form)
        self.btnSampleImage.clicked.connect(self._choose_sample_image)
        self.btnSampleRefresh.clicked.connect(self._refresh_samples)

        # Customer CRUD
        self.btnCusSave.clicked.connect(self._save_customer)
        self.btnCusRemove.clicked.connect(self._remove_customer)
        self.btnCusSearch.clicked.connect(self._search_customer)
        self.btnCusClear.clicked.connect(self._clear_customer_form)
        self.btnCusRefresh.clicked.connect(self._refresh_customers)

        # Employee CRUD
        self.btnEmpSave.clicked.connect(self._save_employee)
        self.btnEmpRemove.clicked.connect(self._remove_employee)
        self.btnEmpSearch.clicked.connect(self._search_employee)
        self.btnEmpClear.clicked.connect(self._clear_employee_form)
        self.btnEmpRefresh.clicked.connect(self._refresh_employees)

        # Charts

        self.btnChartFeedback.clicked.connect(self._chart_feedback)
        self.btnChartRevenue.clicked.connect(self._chart_revenue)

        # Orders — [3] THÊM MỚI
        self.btnOrdersRefresh.clicked.connect(self._refresh_orders)
        self.btnOrdersSearch.clicked.connect(self._search_orders)
        self.tableOrders.itemSelectionChanged.connect(self._show_order_detail)  # click row → popup bill

        # Logout
        self.btnLogout.clicked.connect(self._logout)

    # ── Form fill from row click ────────────────────────────────────
    def _fill_sample_form(self):
        row = self.tableSamples.currentRow()
        if row < 0: return
        self.inputSampleID.setText(self.tableSamples.item(row, 0).text())
        self.inputSampleName.setText(self.tableSamples.item(row, 1).text())
        self.inputSamplePrice.setText(self.tableSamples.item(row, 2).text())
        season = self.tableSamples.item(row, 3).text()
        idx = self.comboSampleSeason.findText(season)
        if idx >= 0:
            self.comboSampleSeason.setCurrentIndex(idx)
        name = self.tableSamples.item(row, 1).text()
        self._load_sample_image_preview(name)

    def _fill_customer_form(self):
        row = self.tableCustomers.currentRow()
        if row < 0: return
        self.inputCusName.setText(self.tableCustomers.item(row, 0).text())
        self.inputCusPhone.setText(self.tableCustomers.item(row, 1).text())
        ctype = self.tableCustomers.item(row, 2).text()
        idx = self.comboCusType.findText(ctype)
        if idx >= 0: self.comboCusType.setCurrentIndex(idx)
        rating = self.tableCustomers.item(row, 3).text()
        idx2 = self.comboCusRating.findText(rating)
        if idx2 >= 0: self.comboCusRating.setCurrentIndex(idx2)
        # Hiện feedback của customer được chọn
        phone = self.tableCustomers.item(row, 1).text()
        cus = self.lc.find_by_phone(phone)
        feedback = (cus.feedback or "—") if cus and cus.feedback else "—"
        self.lblCusFeedbackValue.setText(feedback)

    def _fill_employee_form(self):
        row = self.tableEmployees.currentRow()
        if row < 0: return
        self.inputEmpID.setText(self.tableEmployees.item(row, 0).text())
        self.inputEmpName.setText(self.tableEmployees.item(row, 1).text())
        self.inputEmpExp.setText(self.tableEmployees.item(row, 2).text())

    # ── SAMPLE CRUD ────────────────────────────────────────────────
    def _save_sample(self):
        sid    = self.inputSampleID.text().strip()
        name   = self.inputSampleName.text().strip()
        price  = self.inputSamplePrice.text().strip()
        season = self.comboSampleSeason.currentText()

        if not all([sid, name, price]):
            QMessageBox.warning(self.Window, "Sample", "ID, Name and Price are required.")
            return
        try:
            price_f = float(price)
        except ValueError:
            QMessageBox.warning(self.Window, "Sample", "Price must be a number.")
            return

        new_s = Sample(sid, name, price_f, season)
        if self.ls.find_item(sid):
            self.ls.update_item(new_s)
            QMessageBox.information(self.Window, "Sample", "Sample updated successfully!")
        else:
            self.ls.add_item(new_s)
            self.ls.export_json()
            QMessageBox.information(self.Window, "Sample", "Sample added successfully!")

        self._display_samples(self.ls.list)

    def _remove_sample(self):
        sid = self.inputSampleID.text().strip()
        if not sid:
            QMessageBox.warning(self.Window, "Sample", "Please select or enter a Sample ID.")
            return
        if not self.ls.find_item(sid):
            QMessageBox.warning(self.Window, "Sample", f"Sample '{sid}' not found.")
            return
        reply = QMessageBox.question(
            self.Window, "Confirm", f"Remove sample '{sid}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.ls.remove_item(sid)
            self._display_samples(self.ls.list)
            self._clear_sample_form()

    def _search_sample(self):
        sid    = self.inputSampleID.text().strip()
        name   = self.inputSampleName.text().strip().lower()
        season = self.comboSampleSeason.currentText()
        result = self.ls.list
        if sid:
            result = [s for s in result if sid.lower() in s.sample_id.lower()]
        if name:
            result = [s for s in result if name in s.name.lower()]
        if sid or name:
            result = [s for s in result if s.season == season]
        if not result:
            QMessageBox.information(self.Window, "Sample", "No samples found.")
        self._display_samples(result)

    def _clear_sample_form(self):
        for w in [self.inputSampleID, self.inputSampleName, self.inputSamplePrice]:
            w.clear()
        self.lblSampleImage.setText("No image")
        self.lblSampleImage.setPixmap(QPixmap())
        self._display_samples(self.ls.list)

    def _load_sample_image_preview(self, sample_name: str):
        from PyQt6.QtCore import Qt
        slug = sample_name.lower().replace(" ", "_")
        for ext in (".jpg", ".png"):
            path = os.path.join(IMG_DIR, slug + ext)
            if os.path.exists(path):
                pix = QPixmap(path).scaled(
                    160, 100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.lblSampleImage.setPixmap(pix)
                self.lblSampleImage.setText("")
                return
        self.lblSampleImage.setText("No image")
        self.lblSampleImage.setPixmap(QPixmap())

    def _choose_sample_image(self):
        name = self.inputSampleName.text().strip()
        if not name:
            QMessageBox.warning(self.Window, "Sample", "Please enter the sample name first.")
            return
        path, _ = QFileDialog.getOpenFileName(
            self.Window, "Choose Image", "",
            "Images (*.jpg *.jpeg *.png)"
        )
        if not path:
            return
        slug = name.lower().replace(" ", "_")
        ext  = os.path.splitext(path)[1].lower()
        dest = os.path.join(IMG_DIR, slug + ext)
        os.makedirs(IMG_DIR, exist_ok=True)
        shutil.copy(path, dest)
        self._load_sample_image_preview(name)
        QMessageBox.information(self.Window, "Image", f"Image saved as {slug}{ext}")

    def _refresh_samples(self):
        self.ls.import_json(self.file_samples)
        self._display_samples(self.ls.list)
        self._clear_sample_form()

    # ── CUSTOMER CRUD ──────────────────────────────────────────────
    def _save_customer(self):
        name   = self.inputCusName.text().strip()
        phone  = self.inputCusPhone.text().strip()
        ctype  = self.comboCusType.currentText()
        rating = int(self.comboCusRating.currentText())

        if not name:
            QMessageBox.warning(self.Window, "Customer", "Name is required.")
            return

        existing = self.lc.find_by_phone(phone) if phone else None
        if existing:
            existing.name     = name
            existing.cus_type = ctype
            existing.rating   = rating
            self.lc.export_json()
            QMessageBox.information(self.Window, "Customer", "Customer updated!")
        else:
            self.lc.add_item(Customer(name, phone, ctype, rating))
            self.lc.export_json()
            QMessageBox.information(self.Window, "Customer", "Customer added!")

        self._display_customers(self.lc.list)

    def _remove_customer(self):
        phone = self.inputCusPhone.text().strip()
        target = self.lc.find_by_phone(phone) if phone else None
        if not target:
            QMessageBox.warning(self.Window, "Customer", "Customer not found by phone.")
            return
        reply = QMessageBox.question(
            self.Window, "Confirm", f"Remove customer '{target.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.lc.remove_item(phone)
            self._display_customers(self.lc.list)
            self._clear_customer_form()

    def _search_customer(self):
        name  = self.inputCusName.text().strip().lower()
        phone = self.inputCusPhone.text().strip()
        ctype = self.comboCusType.currentText()
        result = self.lc.list
        if name:  result = [c for c in result if name in c.name.lower()]
        if phone: result = [c for c in result if str(c.phone) == phone]
        if (name or phone) and ctype:
            result = [c for c in result if c.cus_type == ctype]
        if not result:
            QMessageBox.information(self.Window, "Customer", "No customers found.")
        self._display_customers(result)

    def _clear_customer_form(self):
        self.inputCusName.clear()
        self.inputCusPhone.clear()
        self.comboCusType.setCurrentIndex(0)
        self.comboCusRating.setCurrentIndex(0)
        self.lblCusFeedbackValue.setText("—")  # reset label feedback
        self._display_customers(self.lc.list)

    def _refresh_customers(self):
        self.lc.import_json(self.file_customers)
        self._display_customers(self.lc.list)
        self._clear_customer_form()

    # ── EMPLOYEE CRUD ──────────────────────────────────────────────
    def _save_employee(self):
        emp_id = self.inputEmpID.text().strip()
        name   = self.inputEmpName.text().strip()
        exp    = self.inputEmpExp.text().strip()

        if not all([emp_id, name]):
            QMessageBox.warning(self.Window, "Employee", "ID and Name are required.")
            return
        try:
            exp_i = int(exp) if exp else 0
        except ValueError:
            QMessageBox.warning(self.Window, "Employee", "Experience must be a number.")
            return

        existing = self.le.find_item(emp_id)
        if existing:
            existing.name       = name
            existing.experience = exp_i
            self.le.export_json()
            QMessageBox.information(self.Window, "Employee", "Employee updated!")
        else:
            self.le.add_item(Employee(emp_id, name, exp_i))
            self.le.export_json()
            QMessageBox.information(self.Window, "Employee", "Employee added!")

        self._display_employees(self.le.list)

    def _remove_employee(self):
        emp_id = self.inputEmpID.text().strip()
        if not emp_id or not self.le.find_item(emp_id):
            QMessageBox.warning(self.Window, "Employee", "Employee not found.")
            return
        reply = QMessageBox.question(
            self.Window, "Confirm", f"Remove employee '{emp_id}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.le.remove_item(emp_id)
            self._display_employees(self.le.list)
            self._clear_employee_form()

    def _search_employee(self):
        emp_id = self.inputEmpID.text().strip()
        name   = self.inputEmpName.text().strip().lower()
        result = self.le.list
        if emp_id: result = [e for e in result if emp_id.lower() in e.emp_id.lower()]
        if name:   result = [e for e in result if name in e.name.lower()]
        if not result:
            QMessageBox.information(self.Window, "Employee", "No employees found.")
        self._display_employees(result)

    def _clear_employee_form(self):
        for w in [self.inputEmpID, self.inputEmpName, self.inputEmpExp]:
            w.clear()
        self._display_employees(self.le.list)

    def _refresh_employees(self):
        self.le.import_json(self.file_employees)
        self._display_employees(self.le.list)
        self._clear_employee_form()

    # ── ORDERS — methods ────────────────────────────────
    def _refresh_orders(self):
        """Load lại orders.json và hiện lên table."""
        self.lo.import_json(self.file_orders)
        self._display_orders(self.lo.list)

    def _search_orders(self):
        """Lọc orders theo tên hoặc SĐT khách nhập vào inputOrderSearch."""
        keyword = self.inputOrderSearch.text().strip().lower()
        if not keyword:
            self._display_orders(self.lo.list)
            return
        result = [
            o for o in self.lo.list
            if keyword in (o.cus_name or "").lower()
            or keyword in (o.cus_phone or "").lower()
        ]
        if not result:
            QMessageBox.information(self.Window, "Orders", "No orders found.")
        self._display_orders(result)

    def _show_order_detail(self):
        """Click 1 row trên tableOrders → hiện popup bill đầy đủ."""
        from PyQt6.QtCore import Qt

        row = self.tableOrders.currentRow()
        if row < 0:
            return
        item = self.tableOrders.item(row, 0)
        if item is None:
            return

        order_id = item.text()
        order = self.lo.find_item(order_id)
        if not order:
            return

        # ── Dialog ────────────────────────────────────────────────
        dlg = QDialog(self.Window)
        dlg.setWindowTitle(f"Bill — {order_id}")
        dlg.setFixedWidth(460)
        dlg.setStyleSheet("background-color: rgb(234, 242, 251);")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        S_BLUE  = "color: rgb(0,0,127);"
        S_DARK  = "color: rgb(20,20,20);"
        S_MUTED = "color: rgb(100,100,140); font-size:11px;"
        S_BOLD  = "font-weight:bold; " + S_BLUE
        S_BTN   = ("QPushButton{background-color:rgb(67,139,196);color:white;"
                   "border-radius:8px;font-size:12px;font-weight:bold;padding:6px 20px;}"
                   "QPushButton:hover{background-color:#4E86B5;}")
        S_TABLE = ("QTableWidget{background:white;border:2px solid rgb(170,210,250);"
                   "border-radius:8px;gridline-color:rgb(215,233,255);color:rgb(0,0,127);}"
                   "QHeaderView::section{background:rgb(167,212,238);color:rgb(0,0,127);"
                   "font-weight:bold;font-size:12px;padding:5px;border:none;}"
                   "QTableWidget::item{background:white;color:rgb(0,0,127);padding:4px;}"
                   "QTableWidget::item:selected{background:rgb(210,233,255);color:rgb(0,0,127);}")

        # ── Header ────────────────────────────────────────────────
        hdr = QLabel("🧾  ORDER BILL")
        hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.setStyleSheet(
            "font-size:16px;font-weight:bold;font-family:Georgia,serif;"
            "color:white;background-color:rgb(67,139,196);"
            "border-radius:8px;padding:10px;"
        )
        lay.addWidget(hdr)

        # ── Info block — text chảy tự nhiên, không chia ô ─────────
        info = QFrame()
        info.setStyleSheet("background:white;border:2px solid rgb(170,210,250);"
                           "border-radius:10px;padding:4px;")
        info_lay = QVBoxLayout(info)
        info_lay.setContentsMargins(14, 10, 14, 10)
        info_lay.setSpacing(5)

        def info_line(label, value, muted=False):
            row_w = QWidget()
            row_w.setStyleSheet("background:transparent;border:none;")
            h = QHBoxLayout(row_w)
            h.setContentsMargins(0, 0, 0, 0); h.setSpacing(6)
            lbl = QLabel(label)
            lbl.setStyleSheet(S_BOLD + "font-size:12px;background:transparent;border:none;")
            lbl.setFixedWidth(110)
            val = QLabel(str(value))
            val.setStyleSheet((S_MUTED if muted else S_DARK) +
                              "font-size:12px;background:transparent;border:none;")
            val.setWordWrap(True)
            h.addWidget(lbl); h.addWidget(val, stretch=1)
            return row_w

        def thin_divider():
            d = QFrame()
            d.setFrameShape(QFrame.Shape.HLine)
            d.setStyleSheet("background:rgb(210,230,250);max-height:1px;border:none;")
            return d

        info_lay.addWidget(info_line("Order ID:",   order.order_id or ""))
        info_lay.addWidget(info_line("Date:",        order.date or "", muted=True))
        info_lay.addWidget(thin_divider())
        info_lay.addWidget(info_line("Customer:",    order.cus_name or "Guest"))
        info_lay.addWidget(info_line("Phone:",       order.cus_phone or "—", muted=True))
        info_lay.addWidget(thin_divider())
        info_lay.addWidget(info_line("Technician:",  order.technician or "Any available"))
        info_lay.addWidget(info_line("Payment:",     order.method or ""))
        lay.addWidget(info)

        # ── Items table — giống tableCart trong MainWindow ─────────
        lbl_items = QLabel("Items ordered:")
        lbl_items.setStyleSheet(S_BOLD + "font-size:12px;")
        lay.addWidget(lbl_items)

        tbl = QTableWidget(0, 3)
        tbl.setHorizontalHeaderLabels(["Item", "Qty", "Amount"])
        tbl.setStyleSheet(S_TABLE)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tbl.verticalHeader().setVisible(False)
        tbl.horizontalHeader().setStretchLastSection(True)
        tbl.setAlternatingRowColors(False)

        for item_str in (order.items or []):
            # parse "White Flora Charm x2 ($80.00)"
            try:
                parts   = item_str.rsplit(" x", 1)         # ["White Flora Charm", "2 ($80.00)"]
                name    = parts[0].strip()
                rest    = parts[1]                          # "2 ($80.00)"
                qty     = rest.split(" ")[0]
                amount  = rest.split("($")[1].rstrip(")")   # "80.00"
            except Exception:
                name, qty, amount = item_str, "", ""

            r = tbl.rowCount(); tbl.insertRow(r)
            tbl.setItem(r, 0, QTableWidgetItem(name))
            qi = QTableWidgetItem(qty)
            qi.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tbl.setItem(r, 1, qi)
            qa = QTableWidgetItem(f"${amount}" if amount else "")
            qa.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            tbl.setItem(r, 2, qa)

        row_h = 30
        header_h = 30
        tbl.setFixedHeight(header_h + row_h * max(tbl.rowCount(), 1) + 4)
        tbl.horizontalHeader().setMinimumSectionSize(60)
        tbl.setColumnWidth(0, 220)
        tbl.setColumnWidth(1, 40)
        lay.addWidget(tbl)

        # ── Tổng tiền  ──────────────────
        total_frame = QFrame()
        total_frame.setStyleSheet("background:white;border:2px solid rgb(170,210,250);"
                                  "border-radius:10px;")
        tf_lay = QVBoxLayout(total_frame)
        tf_lay.setContentsMargins(14, 10, 14, 10); tf_lay.setSpacing(5)

        def total_line(label, value, big=False):
            row_w = QWidget()
            row_w.setStyleSheet("background:transparent;border:none;")
            h = QHBoxLayout(row_w)
            h.setContentsMargins(0,0,0,0); h.setSpacing(0)
            lbl = QLabel(label)
            lbl.setStyleSheet(("font-size:14px;" if big else "font-size:12px;") +
                              S_BOLD + "background:transparent;border:none;")
            val = QLabel(value)
            val.setStyleSheet(("font-size:15px;font-weight:bold;color:rgb(67,139,196);"
                               if big else "font-size:12px;" + S_DARK) +
                              "background:transparent;border:none;")
            h.addWidget(lbl); h.addStretch(); h.addWidget(val)
            return row_w

        tf_lay.addWidget(total_line("Subtotal", f"${order.subtotal:.2f}"))
        if order.discount and order.discount > 0:
            tf_lay.addWidget(total_line("Discount (VIP)", f"– ${order.discount:.2f}"))
        tf_lay.addWidget(thin_divider())
        tf_lay.addWidget(total_line("TOTAL", f"${order.total:.2f}", big=True))
        lay.addWidget(total_frame)

        # ── Close ──────────────────────────────────────────────────
        btn_close = QPushButton("Close")
        btn_close.setStyleSheet(S_BTN)
        btn_close.clicked.connect(dlg.accept)
        lay.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)

        dlg.exec()


    # ── CHARTS ─────────────────────────────────────────────────────
    def _clear_chart_area(self):
        if self._current_fig:
            plt.close(self._current_fig)
            self._current_fig = None
        lay = self.tabStats.layout()
        while lay.count() > 2:
            item = lay.takeAt(lay.count() - 1)
            if item.widget():
                item.widget().deleteLater()




    def _chart_feedback(self):
        self._clear_chart_area()
        star_counts = [0] * 5
        for c in self.lc.list:
            try:
                s = int(c.rating)
                if 1 <= s <= 5:
                    star_counts[s - 1] += 1
            except (TypeError, ValueError):
                pass

        if sum(star_counts) == 0:
            QMessageBox.information(self.Window, "Chart", "No rating data yet.")
            return

        labels = ["1 ★", "2 ★", "3 ★", "4 ★", "5 ★"]
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"]
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, star_counts, color=colors, edgecolor="white", linewidth=0.8)
        ax.set_title("Customer Ratings", fontsize=12, fontweight="bold", pad=10)
        ax.set_ylabel("Number of customers")
        ax.yaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        for bar, v in zip(bars, star_counts):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                        str(v), ha='center', va='bottom', fontsize=9)
        fig.tight_layout()
        self._current_fig = fig
        canvas = FigureCanvas(fig)
        self.tabStats.layout().addWidget(canvas)


    def _chart_revenue(self):
        self._clear_chart_area()

        # Load orders mới nhất từ file
        self.lo.import_json(self.file_orders)

        if not self.lo.list:
            QMessageBox.information(self.Window, "Chart",
                                    "No orders yet.\nRevenue chart will appear after the first payment.")
            return

        # Tạo map: tên sản phẩm → season để tra nhanh
        season_map = {s.name: s.season for s in self.ls.list}

        seasons = ["Spring", "Summer", "Autumn", "Winter", "Other"]
        revenue = {s: 0.0 for s in seasons}

        for order in self.lo.list:
            for item_str in (order.items or []):

                try:
                    item_name = item_str.split(" x")[0].strip()
                    season    = season_map.get(item_name, "Other")

                    amount    = float(item_str.split("($")[1].rstrip(")"))
                    revenue[season] += amount
                except (IndexError, ValueError):

                    pass

        # Chỉ vẽ các season có doanh thu > 0
        labels = [s for s in seasons if revenue[s] > 0]
        values = [revenue[s] for s in labels]

        if not values:
            QMessageBox.information(self.Window, "Chart", "No revenue data to display.")
            return

        colors = {
            "Spring": "#f9a8d4",
            "Summer": "#fde68a",
            "Autumn": "#d97706",
            "Winter": "#93c5fd",
            "Other":  "#c4b5fd",
        }
        bar_colors = [colors.get(l, "#aaa") for l in labels]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=bar_colors, edgecolor="white", linewidth=0.8)
        ax.set_title("Actual Revenue by Season ($)", fontsize=12, fontweight="bold", pad=10)
        ax.set_ylabel("Revenue ($)")
        ax.yaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"${v:,.0f}", ha='center', va='bottom', fontsize=8)
        fig.tight_layout()
        self._current_fig = fig
        canvas = FigureCanvas(fig)
        self.tabStats.layout().addWidget(canvas)


    # ── Logout ─────────────────────────────────────────────────────
    def _logout(self):
        reply = QMessageBox.question(
            self.Window, "Logout",
            "Return to login screen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.login_window_ex.LoginWindow.show()
            self.Window.close()
