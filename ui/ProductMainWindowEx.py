from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from matplotlib import pyplot as plt

from models.customers import Customers
from models.customer import Customer
from models.employee import Employee
from models.sample import Sample
from models.samples import Samples
from models.employees import Employees

from ui.ProductMainWindow import Ui_MainWindow


class ProductMainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.file_name_cus = "../datasets/customers.json"
        self.file_name_samples = "../datasets/samples.json"
        self.file_name_emp = "../datasets/employees.json"

        self.cus = Customers()
        self.lp = Samples()
        self.emp = Employees()
        self.current_samples = []
        self.current_customers = []
        self.current_employees = []

        self.cus.import_json(self.file_name_cus)
        self.lp.import_json(self.file_name_samples)
        self.emp.import_json(self.file_name_emp)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.display_samples()
        self.display_customers()
        self.display_employees()

        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    # ================= SIGNAL =================
    def setupSignalAndSlot(self):

        self.tableWidgetSample.itemSelectionChanged.connect(self.process_sample_detail)
        self.tableWidgetCustomer.itemSelectionChanged.connect(self.process_customer_detail)
        self.tableWidgetEmployee.itemSelectionChanged.connect(self.process_employee_detail)

        # SAMPLE
        self.pushButtonSampleSave.clicked.connect(self.save_sample)
        self.pushButtonSampleRemove.clicked.connect(self.remove_sample)
        self.pushButtonSampleSearch.clicked.connect(self.search_sample)

        # CUSTOMER
        self.pushButtonCustomerSave.clicked.connect(self.save_customer)
        self.pushButtonCustomerRemove.clicked.connect(self.remove_customer)
        self.pushButtonCustomerSearch.clicked.connect(self.search_customer)

        # EMPLOYEE
        self.pushButtonEmployeeSave.clicked.connect(self.save_employee)
        self.pushButtonEmployeeRemove.clicked.connect(self.remove_employee)
        self.pushButtonEmployeeSearch.clicked.connect(self.search_employee)

        # CHART SAMPLE
        if hasattr(self, "pushButtonSampleQuantity"):
            self.pushButtonSampleQuantity.clicked.connect(self.show_sample_chart)

        # CHART REVENUE
        if hasattr(self, "pushButtonOpenChartFeedback_4"):
            self.pushButtonOpenChartFeedback_4.clicked.connect(self.show_revenue_chart)

        # CHART FEEDBACK (BAR)
        if hasattr(self, "pushButtonOpenChartFeedback"):
            self.pushButtonOpenChartFeedback.clicked.connect(self.show_feedback_chart)

        # CLOSE
        if hasattr(self, "pushButtonCloseWindow"):
            self.pushButtonCloseWindow.clicked.connect(self.confirm_close_window)

    # ================= PROCESS DETAIL =================
    def process_sample_detail(self):
        row = self.tableWidgetSample.currentRow()
        if row < 0 or row >= len(self.current_samples):
            return

        s = self.current_samples[row]

        self.lineEditSampleID.setText(str(s.SampleID))
        self.lineEditSampleName.setText(str(s.SampleName))
        self.lineEditPrice.setText(str(s.SamplePrice))
        self.lineEditSampleQuantity.setText(str(s.SampleQuantity))

    def process_customer_detail(self):
        row = self.tableWidgetCustomer.currentRow()
        if row < 0 or row >= len(self.current_customers):
            return

        c = self.current_customers[row]

        self.lineEditCustomerUserName.setText(str(c.CustomerUserName))
        self.lineEditPhoneNumber.setText(str(c.PhoneNumber))
        self.lineEditType.setText(str(c.Type))

    def process_employee_detail(self):
        row = self.tableWidgetEmployee.currentRow()
        if row < 0 or row >= len(self.current_employees):
            return

        e = self.current_employees[row]

        self.lineEditEmployeeID.setText(str(e.EmployeeId))
        self.lineEditEmployeeName.setText(str(e.EmployeeName))
        self.lineEditExperience.setText(str(e.Experience))
        self.lineEditCustomerBooked.setText(str(e.CustomerBooked))

    # ================= DISPLAY =================
    def display_samples(self, samples_list=None):
        if samples_list is None:
            samples_list = self.lp.list

        self.current_samples = samples_list
        self.tableWidgetSample.setRowCount(0)

        for it in self.current_samples:
            row = self.tableWidgetSample.rowCount()
            self.tableWidgetSample.insertRow(row)

            self.tableWidgetSample.setItem(row, 0, QTableWidgetItem(str(it.SampleName)))
            self.tableWidgetSample.setItem(row, 1, QTableWidgetItem(str(it.SampleID)))
            self.tableWidgetSample.setItem(row, 2, QTableWidgetItem(str(it.SamplePrice)))
            self.tableWidgetSample.setItem(row, 3, QTableWidgetItem(str(it.SampleQuantity)))

    def display_customers(self, customers_list=None):
        if customers_list is None:
            customers_list = self.cus.list

        self.current_customers = customers_list
        self.tableWidgetCustomer.setRowCount(0)

        for it in self.current_customers:
            row = self.tableWidgetCustomer.rowCount()
            self.tableWidgetCustomer.insertRow(row)

            self.tableWidgetCustomer.setItem(row, 0, QTableWidgetItem(str(it.CustomerUserName)))
            self.tableWidgetCustomer.setItem(row, 1, QTableWidgetItem(str(it.PhoneNumber)))
            self.tableWidgetCustomer.setItem(row, 2, QTableWidgetItem(str(it.Type)))

    def display_employees(self, employees_list=None):
        if employees_list is None:
            employees_list = self.emp.list

        self.current_employees = employees_list
        self.tableWidgetEmployee.setRowCount(0)

        for it in self.current_employees:
            row = self.tableWidgetEmployee.rowCount()
            self.tableWidgetEmployee.insertRow(row)

            self.tableWidgetEmployee.setItem(row, 0, QTableWidgetItem(str(it.EmployeeId)))
            self.tableWidgetEmployee.setItem(row, 1, QTableWidgetItem(str(it.EmployeeName)))
            self.tableWidgetEmployee.setItem(row, 2, QTableWidgetItem(str(it.Experience)))
            self.tableWidgetEmployee.setItem(row, 3, QTableWidgetItem(str(it.CustomerBooked)))

    # ================= SAMPLE CRUD =================
    def save_sample(self):
        QMessageBox.information(self.MainWindow, "Info", "Save Sample clicked")

    def remove_sample(self):
        QMessageBox.information(self.MainWindow, "Info", "Remove Sample clicked")

    def search_sample(self):
        QMessageBox.information(self.MainWindow, "Info", "Search Sample clicked")

    # ================= CUSTOMER CRUD =================
    def save_customer(self):
        QMessageBox.information(self.MainWindow, "Info", "Save Customer clicked")

    def remove_customer(self):
        QMessageBox.information(self.MainWindow, "Info", "Remove Customer clicked")

    def search_customer(self):
        QMessageBox.information(self.MainWindow, "Info", "Search Customer clicked")

    # ================= EMPLOYEE CRUD =================
    def save_employee(self):
        QMessageBox.information(self.MainWindow, "Info", "Save Employee clicked")

    def remove_employee(self):
        QMessageBox.information(self.MainWindow, "Info", "Remove Employee clicked")

    def search_employee(self):
        QMessageBox.information(self.MainWindow, "Info", "Search Employee clicked")

    # ================= SAMPLE CHART =================
    def show_sample_chart(self):

        names = []
        quantities = []

        for s in self.lp.list:
            names.append(str(s.SampleName))
            quantities.append(int(s.SampleQuantity))

        plt.figure(figsize=(8,5))
        plt.bar(names, quantities)
        plt.title("Sample Quantity Statistics")
        plt.xlabel("Sample Name")
        plt.ylabel("Quantity")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # ================= REVENUE CHART =================
    def show_revenue_chart(self):

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        revenues = [0] * 12

        for i, s in enumerate(self.lp.list):
            price = int(s.SamplePrice)
            quantity = int(s.SampleQuantity)

            revenue = price * quantity

            month_index = i % 12
            revenues[month_index] += revenue

        plt.figure(figsize=(8, 5))

        plt.bar(months, revenues, color="skyblue")

        plt.title("Revenue Statistics by Month")
        plt.xlabel("Month")
        plt.ylabel("Revenue")

        plt.tight_layout()
        plt.show()

    # ================= FEEDBACK BAR CHART =================
    def show_feedback_chart(self):

        star_counts = [0, 0, 0, 0, 0]

        for c in self.cus.list:
            try:
                star = int(c.Rating)

                if 1 <= star <= 5:
                    star_counts[star - 1] += 1

            except:
                pass

        stars = ["1⭐", "2⭐", "3⭐", "4⭐", "5⭐"]

        if sum(star_counts) == 0:
            QMessageBox.information(self.MainWindow, "Info", "No feedback data")
            return

        plt.figure(figsize=(7, 5))

        bars = plt.bar(stars, star_counts, color="gold")

        plt.title("Customer Feedback Rating")
        plt.xlabel("Star Rating")
        plt.ylabel("Number of Customers")

        plt.yticks(range(0, max(star_counts) + 1))

        for i, v in enumerate(star_counts):
            plt.text(i, v + 0.05, str(v), ha='center')

        plt.tight_layout()
        plt.show()
    # ================= EXIT =================
    def confirm_close_window(self):

        reply = QMessageBox.question(
            self.MainWindow,
            "Confirm Exit",
            "Are you sure you want to close the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.back_to_login()

    def back_to_login(self):

        from ui.MainWindowLoginEmployeeEx import MainWindowLoginEx
        self.login_window = MainWindowLoginEx()
        self.login_window.show()
        self.MainWindow.close()

    def closeEvent(self, event):

        reply = QMessageBox.question(
            self.MainWindow,
            "Confirm Exit",
            "Are you sure you want to close the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.back_to_login()
            event.accept()
        else:
            event.ignore()