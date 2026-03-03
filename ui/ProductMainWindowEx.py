from PyQt6.QtWidgets import QTableWidgetItem
from models.customers import Customers
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
        self.cus.import_json(self.file_name_cus)
        self.lp.import_json(self.file_name_samples)
        self.emp.import_json(self.file_name_emp)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        # populate the samples, customers and employees tables and wire signals
        self.display_samples()
        self.display_customers()
        self.display_employees()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.tableWidgetSample.itemSelectionChanged.connect(self.process_sample_detail)
        self.tableWidgetCustomer.itemSelectionChanged.connect(self.process_customer_detail)
        self.tableWidgetEmployee.itemSelectionChanged.connect(self.process_employee_detail)

    def process_sample_detail(self):
        selected_row = self.tableWidgetSample.currentRow()
        if selected_row < 0 or selected_row >= len(self.lp.list):
            return
        s = self.lp.list[selected_row]
        widget = getattr(self, 'lineEditSampleID', None)
        if widget:
            widget.setText(str(s.SampleID))
        widget = getattr(self, 'lineEditSampleName', None)
        if widget:
            widget.setText(str(s.SampleName))
        widget = getattr(self, 'lineEditPrice', None)
        if widget:
            widget.setText(str(s.SamplePrice))
        # quantity field in UI is lineEditSampleQuantity
        widget = getattr(self, 'lineEditSampleQuantity', None)
        if widget:
            widget.setText(str(s.SampleQuantity))

    def process_customer_detail(self):
        selected_row = self.tableWidgetCustomer.currentRow()
        if selected_row < 0 or selected_row >= len(self.cus.list):
            return
        c = self.cus.list[selected_row]
        widget = getattr(self, 'lineEditCustomerUserName', None)
        if widget:
            widget.setText(str(c.CustomerUserName))
        widget = getattr(self, 'lineEditCustomerPassword', None)
        if widget:
            widget.setText(str(c.Password))
        widget = getattr(self, 'lineEditPhoneNumber', None)
        if widget:
            widget.setText(str(c.PhoneNumber))

    def process_employee_detail(self):
        selected_row = self.tableWidgetEmployee.currentRow()
        if selected_row < 0 or selected_row >= len(self.emp.list):
            return
        e = self.emp.list[selected_row]
        widget = getattr(self, 'lineEditEmployeeID', None)
        if widget:
            widget.setText(str(e.EmployeeId))
        widget = getattr(self, 'lineEditEmployeeName', None)
        if widget:
            widget.setText(str(e.EmployeeName))
        widget = getattr(self, 'lineEditExperience', None)
        if widget:
            widget.setText(str(e.Experience))
        widget = getattr(self, 'lineEditCustomerBooked', None)
        if widget:
            widget.setText(str(e.CustomerBooked))

    def display_samples(self):
        self.tableWidgetSample.setRowCount(0)
        for it in self.lp.list:
            new_row_index = self.tableWidgetSample.rowCount()
            self.tableWidgetSample.insertRow(new_row_index)
            cell_name = QTableWidgetItem(str(it.SampleName))
            cell_id = QTableWidgetItem(str(it.SampleID))
            cell_price = QTableWidgetItem(str(it.SamplePrice))
            cell_quantity = QTableWidgetItem(str(it.SampleQuantity))
            self.tableWidgetSample.setItem(new_row_index, 0, cell_name)
            self.tableWidgetSample.setItem(new_row_index, 1, cell_id)
            self.tableWidgetSample.setItem(new_row_index, 2, cell_price)
            self.tableWidgetSample.setItem(new_row_index, 3, cell_quantity)
        try:
            self.tableWidgetSample.resizeColumnsToContents()
        except Exception:
            pass

    def display_customers(self):
        self.tableWidgetCustomer.setRowCount(0)
        for it in self.cus.list:
            new_row_index = self.tableWidgetCustomer.rowCount()
            self.tableWidgetCustomer.insertRow(new_row_index)
            cell_user = QTableWidgetItem(str(it.CustomerUserName))
            cell_pwd = QTableWidgetItem(str(it.Password))
            cell_phone = QTableWidgetItem(str(it.PhoneNumber))
            self.tableWidgetCustomer.setItem(new_row_index, 0, cell_user)
            self.tableWidgetCustomer.setItem(new_row_index, 1, cell_pwd)
            self.tableWidgetCustomer.setItem(new_row_index, 2, cell_phone)
        try:
            self.tableWidgetCustomer.resizeColumnsToContents()
        except Exception:
            pass

    def display_employees(self):
        self.tableWidgetEmployee.setRowCount(0)
        for it in self.emp.list:
            new_row_index = self.tableWidgetEmployee.rowCount()
            self.tableWidgetEmployee.insertRow(new_row_index)
            cell_id = QTableWidgetItem(str(it.EmployeeId))
            cell_name = QTableWidgetItem(str(it.EmployeeName))
            cell_exp = QTableWidgetItem(str(it.Experience))
            cell_booked = QTableWidgetItem(str(it.CustomerBooked))
            self.tableWidgetEmployee.setItem(new_row_index, 0, cell_id)
            self.tableWidgetEmployee.setItem(new_row_index, 1, cell_name)
            self.tableWidgetEmployee.setItem(new_row_index, 2, cell_exp)
            self.tableWidgetEmployee.setItem(new_row_index, 3, cell_booked)
        try:
            self.tableWidgetEmployee.resizeColumnsToContents()
        except Exception:
            pass
