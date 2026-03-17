import os
import shutil
import matplotlib

from nail_shop.nail_shop.models.customer import Customer
from nail_shop.nail_shop.models.customers import Customers
from nail_shop.nail_shop.models.employee import Employee
from nail_shop.nail_shop.models.employees import Employees
from nail_shop.nail_shop.models.sample import Sample
from nail_shop.nail_shop.models.samples import Samples
from nail_shop.nail_shop.ui.ProductMainWindow import Ui_ProductMainWindow

matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QTableWidgetItem, QMessageBox, QVBoxLayout, QFileDialog
)
from PyQt6.QtGui import QPixmap



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR  = os.path.join(BASE_DIR, "..", "images")


class ProductMainWindowEx(Ui_ProductMainWindow):
    def __init__(self, login_window_ex):
        self.login_window_ex  = login_window_ex
        self.file_samples     = "datasets/samples.json"
        self.file_customers   = "datasets/customers.json"
        self.file_employees   = "datasets/employees.json"

        self.ls = Samples()
        self.lc = Customers()
        self.le = Employees()

        self.ls.import_json(self.file_samples)
        self.lc.import_json(self.file_customers)
        self.le.import_json(self.file_employees)

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
        self.btnChartSamples.clicked.connect(self._chart_samples)
        self.btnChartFeedback.clicked.connect(self._chart_feedback)
        self.btnChartRevenue.clicked.connect(self._chart_revenue)

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
        # Hiện preview ảnh nếu có
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
            self.ls.update_item(new_s)   # update_item đã gọi export_json() bên trong
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
        if season:
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
        """Hiện preview ảnh trong form khi click row."""
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
        """Mở file dialog chọn ảnh → copy vào images/ với tên slug đúng."""
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
        name  = self.inputCusName.text().strip()
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
        # Chỉ lọc type nếu người dùng đã nhập tên hoặc SĐT (tránh lọc mặc định Normal)
        if (name or phone) and ctype:
            result = [c for c in result if c.cus_type == ctype]
        if not result:
            QMessageBox.information(self.Window, "Customer", "No customers found.")
        self._display_customers(result)

    def _clear_customer_form(self):
        self.inputCusName.clear()
        self.inputCusPhone.clear()
        self.comboCusType.setCurrentIndex(0)    # Normal
        self.comboCusRating.setCurrentIndex(0)  # 0
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

    # ── CHARTS ─────────────────────────────────────────────────────
    def _clear_chart_area(self):
        if self._current_fig:
            plt.close(self._current_fig)
            self._current_fig = None
        # Remove old canvas from stats tab
        lay = self.tabStats.layout()
        while lay.count() > 2:          # keep label + btn row
            item = lay.takeAt(lay.count() - 1)
            if item.widget():
                item.widget().deleteLater()

    def _chart_samples(self):
        self._clear_chart_area()
        names  = [s.name[:14] + "…" if len(s.name) > 14 else s.name for s in self.ls.list]
        prices = [s.price for s in self.ls.list]
        colors = ["#A7D4F0"] * len(prices)

        fig, ax = plt.subplots(figsize=(9, 4))
        bars = ax.bar(names, prices, color=colors, edgecolor="#438bc4", linewidth=0.6)
        ax.set_title("Sample Prices ($)", fontsize=12, fontweight="bold", pad=10)
        ax.set_ylabel("Price ($)")
        ax.tick_params(axis='x', rotation=40, labelsize=7)
        ax.yaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        for bar, p in zip(bars, prices):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"${p}", ha='center', va='bottom', fontsize=7)
        fig.tight_layout()
        self._current_fig = fig
        canvas = FigureCanvas(fig)
        self.tabStats.layout().addWidget(canvas)

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
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        # Doanh thu ước tính = tổng giá các mẫu theo mùa
        revenue = {s: 0.0 for s in seasons}
        for s in self.ls.list:
            if s.season in revenue:
                revenue[s.season] += s.price

        colors = ["#f9a8d4", "#fde68a", "#d97706", "#93c5fd"]
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(seasons, [revenue[s] for s in seasons],
                      color=colors, edgecolor="white", linewidth=0.8)
        ax.set_title("Total Sample Price by Season ($)", fontsize=12, fontweight="bold", pad=10)
        ax.set_ylabel("Total Price ($)")
        ax.yaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        for bar, s in zip(bars, seasons):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"${revenue[s]:,.0f}", ha='center', va='bottom', fontsize=8)
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
