import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QScrollArea
from PyQt6 import QtCore, QtWidgets
from models.customers import Customers
from ui.FeedbackWindow import Ui_RatingUI
from ui.MainWindow import Ui_MainWindow
from ui.PaymentWindow import Ui_PaymentWindow
from ui.SelfCustomWindow import Ui_SelfCustomWindow


class TechnicianWindow(QtWidgets.QWidget):

    def __init__(self, parent_logic):
        super().__init__()

        self.parent_logic = parent_logic

        self.setWindowTitle("Select Technician")
        self.resize(400, 300)

        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Technician", "Experience", "Status"])

        layout.addWidget(self.table)

        self.load_staff()

        self.table.cellDoubleClicked.connect(self.choose_staff)

    def load_staff(self):
        technicians = [
            ("Anna", "5 years", "Available"),
            ("Lisa", "3 years", "Available"),
            ("Sophia", "4 years", "Busy"),
            ("Emma", "6 years", "Available")
        ]

        self.table.setRowCount(len(technicians))

        for row, tech in enumerate(technicians):
            self.table.setItem(row, 0, QTableWidgetItem(tech[0]))
            self.table.setItem(row, 1, QTableWidgetItem(tech[1]))
            self.table.setItem(row, 2, QTableWidgetItem(tech[2]))

    def choose_staff(self, row, column):
        name = self.table.item(row, 0).text()

        self.parent_logic.set_technician(name)

        self.close()
# FEEDBACK WINDOW
class FeedbackWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RatingUI()
        self.ui.setupUi(self)

        self.selected_stars = 0
        self.star_btns = [
            self.ui.star_1,
            self.ui.star_2,
            self.ui.star_3,
            self.ui.star_4,
            self.ui.star_5
        ]

        for i, btn in enumerate(self.star_btns):
            btn.clicked.connect(lambda checked, idx=i+1: self.update_stars(idx))

        self.ui.btnSubmit.clicked.connect(self.submit_action)

    def update_stars(self, count):
        self.selected_stars = count

        for i, btn in enumerate(self.star_btns):
            if i < count:
                btn.setStyleSheet("color: gold; font-size: 35px; border:none; background:transparent;")
            else:
                btn.setStyleSheet("color: #333; font-size: 35px; border:none; background:transparent;")

    def submit_action(self):

        if self.selected_stars == 0:
            QMessageBox.warning(self, "Notice", "Please select a rating!")
            return

        QMessageBox.information(self, "Thank you", "Thank you for your feedback!")
        self.close()


# ===============================
# PAYMENT WINDOW
# ===============================
class PaymentWindow(QMainWindow):

    def __init__(self, total_amount):
        super().__init__()

        self.ui = Ui_PaymentWindow()
        self.ui.setupUi(self)

        self.ui.lblTotalValue.setText(total_amount)
        self.ui.btnConfirm.clicked.connect(self.confirm_payment)

    def confirm_payment(self):

        QMessageBox.information(
            self,
            "Success",
            "Payment successful! We are preparing your service."
        )

        self.close()

        self.fb_screen = FeedbackWindow()
        self.fb_screen.show()


# ===============================
# CUSTOM NAIL WINDOW
# ===============================
class SelfCustomWindow(QMainWindow):

    def __init__(self, parent_logic):
        super().__init__()

        self.ui = Ui_SelfCustomWindow()
        self.ui.setupUi(self)

        self.parent_logic = parent_logic

        # chọn màu
        self.setup_color_buttons()

        # upload ảnh
        self.ui.buychocolatebalance_44.clicked.connect(self.upload_photo)

        # confirm
        self.ui.buychocolatebalance_45.clicked.connect(self.confirm_custom)


    # =========================
    # SETUP COLOR BUTTONS
    # =========================
    def setup_color_buttons(self):

        for i in range(1, 26):

            btn = getattr(self.ui, f"color_{i}", None)

            if btn:
                btn.clicked.connect(
                    lambda checked, b=btn: self.select_color(b)
                )


    # =========================
    # CHỌN MÀU
    # =========================
    def select_color(self, button):

        color = button.palette().button().color().name()

        self.ui.txtSelectedColor.setText(color)


    # =========================
    # UPLOAD PHOTO
    # =========================
    def upload_photo(self):

        from PyQt6.QtWidgets import QFileDialog
        from PyQt6.QtGui import QPixmap

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file_name:

            pixmap = QPixmap(file_name)

            self.ui.imagecoffee_43.setPixmap(pixmap)

            self.ui.imagecoffee_43.setScaledContents(True)


    # =========================
    # CONFIRM CUSTOM
    # =========================
    def confirm_custom(self):

        style = self.ui.chooseTheStyleComboBox.currentText()
        length = self.ui.chooseTheStyleComboBox_2.currentText()
        color = self.ui.txtSelectedColor.text()
        description = self.ui.textEdit.toPlainText()

        item_desc = f"Custom Nail: {style}, {length}, {color}"

        if description:
            item_desc += f" | Note: {description}"

        self.parent_logic.add_to_cart(item_desc, 50.00)

        QMessageBox.information(self, "Added", "Custom nail added to cart!")

        self.close()
# ===============================
# MAIN WINDOW
# ===============================
class MainWindowEx(Ui_MainWindow):

    def __init__(self):
        self.file_name_cus = "../datasets/customers.json"
        self.cus = Customers()
        self.cus.import_json(self.file_name_cus)
        super().__init__()
        self.cart = []
        self.total_money = 0


    def setupUi(self, MainWindow):

        super().setupUi(MainWindow)

        self.MainWindow = MainWindow

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(self.centralwidget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;}")

        MainWindow.setCentralWidget(scroll)

        # Tổng tiền ban đầu
        self.lineEdit_TotalBill.setText("0.00$")

        # ========================
        # CONNECT BUTTONS
        # ========================

        self.pushButton_TB_9.clicked.connect(self.open_payment)
        self.pushButton_TB_10.clicked.connect(self.remove_from_cart)
        self.pushButton_loadCusType_2.clicked.connect(self.calculate_total)


        self.buychocolatebalance_79.clicked.connect(self.open_self_custom)
        self.pushButton_TB_11.clicked.connect(self.open_technician)
        self.menuMore_about_us.aboutToShow.connect(self.show_about_us)
        self.Spring.clicked.connect(self.show_spring)
        self.Summer.clicked.connect(self.show_summer)
        self.Autumn.clicked.connect(self.show_autumn)
        self.Winter.clicked.connect(self.show_winter)
        self.pushButton_TB_16.clicked.connect(self.process_logout)
        # ========================
        # ADD PRODUCTS
        # ========================

        # SPRING
        self.buychocolatebalance_94.clicked.connect(
            lambda: self.add_to_cart("White Flora Charm", 36)
        )

        self.buychocolatebalance_95.clicked.connect(
            lambda: self.add_to_cart("Yellow Daisy Garden", 30)
        )

        self.buychocolatebalance_96.clicked.connect(
            lambda: self.add_to_cart("Silver Ribbon Dew", 25)
        )

        # SUMMER
        self.buychocolatebalance_90.clicked.connect(
            lambda: self.add_to_cart("Pink Crystal Fairy", 40)
        )

        self.buychocolatebalance_91.clicked.connect(
            lambda: self.add_to_cart("Sparkling Starlight", 37)
        )

        # AUTUMN
        self.buychocolatebalance_92.clicked.connect(
            lambda: self.add_to_cart("Green Matcha Muse", 36)
        )

        self.buychocolatebalance_93.clicked.connect(
            lambda: self.add_to_cart("Sunny Side Up", 26)
        )

        # WINTER
        self.buychocolatebalance_97.clicked.connect(
            lambda: self.add_to_cart("Ocean Pearl Dream", 40)
        )

        self.buychocolatebalance_89.clicked.connect(
            lambda: self.add_to_cart("Cosmic Marble Pink", 36)
        )
        self.buychocolatebalance_84.clicked.connect(
            lambda: self.add_to_cart("Butterfly Garden Glow ", 36)
        )
        self.buychocolatebalance_83.clicked.connect(
            lambda: self.add_to_cart("Creamy Heart Pearl", 32)
        )

        self.buychocolatebalance_99.clicked.connect(
            lambda: self.add_to_cart("Winter Snowman", 30)
        )

        self.buychocolatebalance_98.clicked.connect(
            lambda: self.add_to_cart("Purple Amethyst Glaze", 36)

        )

        # ========================
        # SEASON PRODUCTS
        # ========================

        self.spring_widgets = [
            self.widget_65,
            self.widget_66,
            self.widget_36,
            self.widget_30,
        ]

        self.summer_widgets = [
            self.widget_31,
            self.widget_33,
            self.widget_37,
            self.widget_39
        ]

        self.autumn_widgets = [
            self.widget_64,
            self.widget_63,
            self.widget_38
        ]

        self.winter_widgets = [
            self.widget_32,
            self.widget_35,
            self.widget_63
        ]
    # ===============================
    # ADD ITEM
    # ===============================
    def add_to_cart(self, item_name, price):

        for index, (name, item_price, quantity) in enumerate(self.cart):

            if name == item_name:

                self.cart[index] = (name, item_price, quantity + 1)

                self.update_cart_display()

                return

        self.cart.append((item_name, price, 1))

        self.update_cart_display()


    # ===============================
    # UPDATE CART TABLE
    # ===============================
    def update_cart_display(self):

        self.tableWidget.setRowCount(0)

        self.total_money = 0

        for name, price, quantity in self.cart:

            row = self.tableWidget.rowCount()

            self.tableWidget.insertRow(row)

            self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(quantity)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(f"{price * quantity}$"))

            self.total_money += price * quantity

        self.lineEdit_TotalBill.setText(f"{self.total_money:.2f}$")


    # ===============================
    # REMOVE ITEM
    # ===============================
    def remove_from_cart(self):

        row = self.tableWidget.currentRow()

        if row < 0:

            QMessageBox.warning(self.MainWindow, "Warning", "Please select an item!")

            return

        del self.cart[row]

        self.update_cart_display()

    # ===============================
    # HIDE ALL PRODUCTS
    # ===============================
    def hide_all_products(self):

        all_widgets = (
                self.spring_widgets
                + self.summer_widgets
                + self.autumn_widgets
                + self.winter_widgets
        )

        for w in all_widgets:
            w.setVisible(False)

    # ===============================
    # SHOW SPRING
    # ===============================
    def show_spring(self):

        self.hide_all_products()

        for w in self.spring_widgets:
            w.setVisible(True)

    def show_summer(self):

        self.hide_all_products()

        for w in self.summer_widgets:
            w.setVisible(True)

    def show_autumn(self):

        self.hide_all_products()

        for w in self.autumn_widgets:
            w.setVisible(True)

    def show_winter(self):

        self.hide_all_products()

        for w in self.winter_widgets:
            w.setVisible(True)
    #SET TECHNICIAN
    def set_technician(self, name):

        self.selected_technician = name

        QMessageBox.information(
            self.MainWindow,
            "Technician Selected",
            f"You selected: {name}"
        )


    # ===============================
    # PAYMENT
    # ===============================
    def open_payment(self):

        if self.total_money <= 0:

            QMessageBox.warning(self.MainWindow, "Empty", "Your cart is empty!")

            return

        self.payment_screen = PaymentWindow(self.lineEdit_TotalBill.text())

        self.payment_screen.show()


    # ===============================
    # CUSTOM NAIL
    # ===============================
    def open_self_custom(self):

        self.custom_screen = SelfCustomWindow(self)

        self.custom_screen.show()


    # ===============================
    # ABOUT US
    # ===============================
    def show_about_us(self):

        about_title = "✨ ABOUT MY NAIL SHOP ✨"

        about_text = (
            "<b>Vision:</b> <i>Elevating Vietnamese Beauty Through Every Stroke</i><br><br>"
            "<b>Professional Team:</b><br>"
            "• Certified technicians<br>"
            "• Latest nail trends<br>"
            "• Premium products<br><br>"
            "<b>Contact:</b><br>"
            "📍 UEL University Village<br>"
            "📞 (+84) 123 456 789<br>"
            "⏰ 08:00 - 21:00"
        )

        msg = QtWidgets.QMessageBox(self.MainWindow)

        msg.setWindowTitle("About Us")

        msg.setTextFormat(QtCore.Qt.TextFormat.RichText)

        msg.setText(about_title)

        msg.setInformativeText(about_text)

        msg.exec()


    def open_technician(self):

        self.tech_window = TechnicianWindow(self)

        self.tech_window.show()
    # SEARCH

    def get_customer_type(self):

        phone = self.lineEdit_PhoneNum_2.text().strip()

        for c in self.cus.list:
            if str(c.PhoneNumber) == phone:
                return c.Type

        return None
    def calculate_total(self):

            cus_type = self.get_customer_type()

            if cus_type is None:
                QMessageBox.warning(self.MainWindow, "Customer", "Customer not found")
                return

            self.lineEdit_CustomerType_3.setText(cus_type)

            total = self.total_money

            if cus_type.lower() == "vip":
                total = total * 0.85

            self.lineEdit_TotalBill.setText(f"{total:.2f}$")
    def show(self):
        self.MainWindow.show()


    # ===============================
    # log out
    # ===============================

    def process_logout(self):
            # Hiển thị hộp thoại xác nhận
            msg = QMessageBox.question(
                self.MainWindow,
                "Confirm Logout",
                "Are you sure you want to log out?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
    
            if msg == QMessageBox.StandardButton.Yes:
                # Import tại đây để tránh lỗi vòng lặp import (circular import)
                from ui.MainWindowLoginEmployeeEx import MainWindowLoginEx
                
                # Khởi tạo lại màn hình Login
                self.login_window = MainWindowLoginEx()
                self.login_window.show()
                
                # Đóng màn hình chính hiện tại
                self.MainWindow.close()
    
    
        
        
