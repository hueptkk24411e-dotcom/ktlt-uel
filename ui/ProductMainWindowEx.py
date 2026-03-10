from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
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

#CHỨC NĂNG Ở SAMPLE
        self.pushButtonSampleSave.clicked.connect(self.save_sample)
        self.pushButtonSampleRemove.clicked.connect(self.remove_sample)
        self.pushButtonSampleSearch.clicked.connect(self.search_sample)

#CHỨC NĂNG Ở CUSTOMER
        self.pushButtonCustomerSave.clicked.connect(self.save_customer)
        self.pushButtonCustomerRemove.clicked.connect(self.remove_customer)
        self.pushButtonCustomerSearch.clicked.connect(self.search_customer)

#CHỨC NĂNG Ở EMPLOYEE
        self.pushButtonEmployeeSave.clicked.connect(self.save_employee)
        self.pushButtonEmployeeRemove.clicked.connect(self.remove_employee)
        self.pushButtonEmployeeSearch.clicked.connect(self.search_employee)



    def process_sample_detail(self):
        selected_row = self.tableWidgetSample.currentRow()
        if selected_row < 0 or selected_row >= len(self.current_samples):
            return
        s = self.current_samples[selected_row]
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
        if selected_row < 0 or selected_row >= len(self.current_customers):
            return
        c = self.current_customers[selected_row]
        widget = getattr(self, 'lineEditCustomerUserName', None)
        if widget:
            widget.setText(str(c.CustomerUserName))
        widget = getattr(self, 'lineEditPhoneNumber', None)
        if widget:
            widget.setText(str(c.PhoneNumber))
        widget = getattr(self, 'lineEditType', None)
        if widget:
            widget.setText(str(c.Type))
    def process_employee_detail(self):
        selected_row = self.tableWidgetEmployee.currentRow()
        if selected_row < 0 or selected_row >= len(self.current_employees):
            return
        e = self.current_employees[selected_row]
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

    def display_samples(self, samples_list=None):
        if samples_list is None:
            samples_list = self.lp.list
        self.current_samples = samples_list
        self.tableWidgetSample.setRowCount(0)
        for it in self.current_samples:
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

    def display_customers(self, customers_list=None):
        if customers_list is None:
            customers_list = self.cus.list
        self.current_customers = customers_list
        self.tableWidgetCustomer.setRowCount(0)
        for it in self.current_customers:
            new_row_index = self.tableWidgetCustomer.rowCount()
            self.tableWidgetCustomer.insertRow(new_row_index)
            cell_user = QTableWidgetItem(str(it.CustomerUserName))
            cell_phone = QTableWidgetItem(str(it.PhoneNumber))
            cell_type = QTableWidgetItem(str(it.Type))
            self.tableWidgetCustomer.setItem(new_row_index, 0, cell_user)
            self.tableWidgetCustomer.setItem(new_row_index, 1, cell_phone)
            self.tableWidgetCustomer.setItem(new_row_index, 2, cell_type)
        try:
            self.tableWidgetCustomer.resizeColumnsToContents()
        except Exception:
            pass

    def display_employees(self, employees_list=None):
        if employees_list is None:
            employees_list = self.emp.list
        self.current_employees = employees_list
        self.tableWidgetEmployee.setRowCount(0)
        for it in self.current_employees:
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

    def save_sample(self):
        sample_id = self.lineEditSampleID.text().strip()
        sample_name = self.lineEditSampleName.text().strip()
        sample_price = self.lineEditPrice.text().strip()
        sample_quantity = self.lineEditSampleQuantity.text().strip()
        if not sample_id or not sample_name or not sample_price or not sample_quantity:
            QMessageBox.warning(self.MainWindow, "Sample", "Sample ID, Sample Name, Sample Price and Sample Quantity are required.")
            return None

        try:
            sample_quantity = int(sample_quantity)
        except ValueError:
            QMessageBox.warning(self.MainWindow, "Sample", "Sample Quantity must be an integer.")
            return None

        # Check if sample exists by ID
        sample = Sample(sample_id, sample_name, sample_price, sample_quantity)
        self.lp.add_item(sample)  # Assumes add_item handles updates if ID exists
        self.lp.export_json("../datasets/samples.json")  # Adjust path as needed
        self.display_samples()  # Refresh the table
        QMessageBox.information(self.MainWindow, "Sample", "Update Successfully!")

    def remove_sample(self):
        sample_id = self.lineEditSampleID.text().strip()
        if not sample_id:
            QMessageBox.warning(self.MainWindow, "Sample", "No sample available")
            return

        # Remove the sample from the list by ID
        self.lp.list = [s for s in self.lp.list if s.SampleID != sample_id]
        self.lp.export_json("../datasets/samples.json")
        self.display_samples()
        QMessageBox.information(self.MainWindow, "Sample", "Remove Successfully!")

    def search_sample(self):
        sample_id = self.lineEditSampleID.text().strip()
        sample_name = self.lineEditSampleName.text().strip()
        sample_price = self.lineEditPrice.text().strip()
        sample_quantity = self.lineEditSampleQuantity.text().strip()

        filtered = self.lp.list

        if sample_id:
            filtered = [s for s in filtered if str(s.SampleID) == sample_id]
        if sample_name:
            filtered = [s for s in filtered if sample_name.lower() in str(s.SampleName).lower()]
        if sample_price:
            filtered = [s for s in filtered if str(s.SamplePrice) == sample_price]
        if sample_quantity:
            filtered = [s for s in filtered if str(s.SampleQuantity) == sample_quantity]

        if not filtered:
            QMessageBox.information(self.MainWindow, "Sample", "No sample available")
            return

        self.display_samples(filtered)

    def save_customer(self):
        customer_username = self.lineEditCustomerUserName.text().strip()
        phone_number = self.lineEditPhoneNumber.text().strip()
        customer_type = self.lineEditType.text().strip()
        if not customer_username or not phone_number or not customer_type:
            QMessageBox.warning(self.MainWindow, "Customer", "Customer UserName, Phone Number and Type are required.")
            return None

        customer = Customer(customer_username, phone_number, customer_type)
        self.cus.add_item(customer)
        self.cus.export_json("../datasets/customers.json")
        self.display_customers()
        QMessageBox.information(self.MainWindow, "Customer", "Update Successfully!")

    def remove_customer(self):
        customer_username = self.lineEditCustomerUserName.text().strip()
        if not customer_username:
            QMessageBox.warning(self.MainWindow, "Customer", "No customer available")
            return

        # Remove the customer from the list by UserName
        self.cus.list = [c for c in self.cus.list if c.CustomerUserName != customer_username]
        self.cus.export_json("../datasets/customers.json")
        self.display_customers()
        QMessageBox.information(self.MainWindow, "Customer", "Remove Successfully!")

    def search_customer(self):
        customer_username = self.lineEditCustomerUserName.text().strip()
        phone_number = self.lineEditPhoneNumber.text().strip()
        customer_type = self.lineEditType.text().strip()

        filtered = self.cus.list

        if customer_username:
            filtered = [c for c in filtered if customer_username.lower() in str(c.CustomerUserName).lower()]
        if phone_number:
            filtered = [c for c in filtered if str(c.PhoneNumber) == phone_number]
        if customer_type:
            filtered = [c for c in filtered if str(c.Type) == customer_type]

        if not filtered:
            QMessageBox.information(self.MainWindow, "Customer", "No customer available")
            return

        self.display_customers(filtered)

    def save_employee(self):
        employee_id = self.lineEditEmployeeID.text().strip()
        employee_name = self.lineEditEmployeeName.text().strip()
        experience = self.lineEditExperience.text().strip()
        customer_booked = self.lineEditCustomerBooked.text().strip()
        if not employee_id or not employee_name or not experience or not customer_booked:
            QMessageBox.warning(self.MainWindow, "Employee", "Employee ID, Name, Experience and Booked Customer are required.")
            return None

        try:
            experience = int(experience)
        except ValueError:
            QMessageBox.warning(self.MainWindow, "Employee", "Experience must be an integer.")
            return None

        employee = Employee(employee_id, employee_name, experience, customer_booked)
        self.emp.add_item(employee)
        self.emp.export_json("../datasets/employees.json")
        self.display_employees()
        QMessageBox.information(self.MainWindow, "Employee", "Update Successfully!")

    def remove_employee(self):
        employee_id = self.lineEditEmployeeID.text().strip()
        if not employee_id:
            QMessageBox.warning(self.MainWindow, "Employee", "No employee available")
            return

        # Remove the employee from the list by ID
        self.emp.list = [e for e in self.emp.list if e.EmployeeId != employee_id]
        self.emp.export_json("../datasets/employees.json")
        self.display_employees()
        QMessageBox.information(self.MainWindow, "Employee", "Remove Successfully!")

    def search_employee(self):
        employee_id = self.lineEditEmployeeID.text().strip()
        employee_name = self.lineEditEmployeeName.text().strip()
        experience = self.lineEditExperience.text().strip()
        customer_booked = self.lineEditCustomerBooked.text().strip()

        filtered = self.emp.list

        if employee_id:
            filtered = [e for e in filtered if str(e.EmployeeId) == employee_id]
        if employee_name:
            filtered = [e for e in filtered if employee_name.lower() in str(e.EmployeeName).lower()]
        if experience:
            filtered = [e for e in filtered if str(e.Experience) == experience]
        if customer_booked:
            filtered = [e for e in filtered if str(e.CustomerBooked) == customer_booked]

        if not filtered:
            QMessageBox.information(self.MainWindow, "Employee", "No employee available")
            return

        self.display_employees(filtered)
