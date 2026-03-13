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
            row = self.tableWidgetCustomer.rowCount()
            self.tableWidgetCustomer.insertRow(row)

            self.tableWidgetCustomer.setItem(row, 0, QTableWidgetItem(str(it.CustomerUserName)))
            self.tableWidgetCustomer.setItem(row, 1, QTableWidgetItem(str(it.PhoneNumber)))
            self.tableWidgetCustomer.setItem(row, 2, QTableWidgetItem(str(it.Type)))
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
            row = self.tableWidgetEmployee.rowCount()
            self.tableWidgetEmployee.insertRow(row)

            self.tableWidgetEmployee.setItem(row, 0, QTableWidgetItem(str(it.EmployeeId)))
            self.tableWidgetEmployee.setItem(row, 1, QTableWidgetItem(str(it.EmployeeName)))
            self.tableWidgetEmployee.setItem(row, 2, QTableWidgetItem(str(it.Experience)))
            self.tableWidgetEmployee.setItem(row, 3, QTableWidgetItem(str(it.CustomerBooked)))
        try:
            self.tableWidgetEmployee.resizeColumnsToContents()
        except Exception:
            pass


    # ================= SAMPLE CRUD =================
    def save_sample(self):
        sample_id = self.lineEditSampleID.text().strip()
        sample_name = self.lineEditSampleName.text().strip()
        sample_price = self.lineEditPrice.text().strip()
        sample_quantity = self.lineEditSampleQuantity.text().strip()
        if not sample_id or not sample_name or not sample_price or not sample_quantity:
            QMessageBox.warning(self.MainWindow, "Sample",
                                "Sample ID, Sample Name, Sample Price and Sample Quantity are required.")
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
            QMessageBox.warning(self.MainWindow, "Employee",
                                "Employee ID, Name, Experience and Booked Customer are required.")
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