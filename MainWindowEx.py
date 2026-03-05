import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QScrollArea
from PyQt6 import QtCore, QtWidgets
from MainWindow import Ui_MainWindow
from PaymentWindow import Ui_PaymentWindow
from SelfCustomWindow import Ui_SelfCustomWindow
from FeedbackWindow import Ui_RatingUI


class FeedbackWindow(QtWidgets.QWidget): # Thay QMainWindow bằng QWidget
    def __init__(self):
        super().__init__()
        self.ui = Ui_RatingUI()
        self.ui.setupUi(self)
        self.selected_stars = 0

        # Đảm bảo các tên object star_1...star_5 khớp chính xác với file FeedbackWindow.py
        self.star_btns = [self.ui.star_1, self.ui.star_2, self.ui.star_3, self.ui.star_4, self.ui.star_5]

        for i, btn in enumerate(self.star_btns):
            btn.clicked.connect(lambda checked, idx=i + 1: self.update_stars(idx))

        self.ui.btnSubmit.clicked.connect(self.submit_action)

    def update_stars(self, count):
        self.selected_stars = count
        for i, btn in enumerate(self.star_btns):
            if i < count:
                # Sao sáng (Vàng)
                btn.setStyleSheet("color: gold; font-size: 35px; background: transparent; border: none;")
            else:
                # Sao tối (Xám/Đen tùy theme)
                btn.setStyleSheet("color: #333; font-size: 35px; background: transparent; border: none;")

    def submit_action(self):
        if self.selected_stars == 0:
            QMessageBox.warning(self, "Notice", "Please select a star rating!")
            return
        QMessageBox.information(self, "Thank you", "Thank you for your feedback!")
        self.close()



class PaymentWindow(QMainWindow):
    def __init__(self, total_amount):
        super().__init__()
        self.ui = Ui_PaymentWindow()
        self.ui.setupUi(self)
        # Hiển thị số tiền từ giỏ hàng sang trang thanh toán
        self.ui.lblTotalValue.setText(total_amount)
        self.ui.btnConfirm.clicked.connect(self.confirm_payment)

    def confirm_payment(self):
        # 1. Thông báo thanh toán thành công
        QMessageBox.information(self, "Success", "Payment successful! We are preparing your service.")

        # 2. Đóng cửa sổ thanh toán
        self.close()

        # 3. Mở cửa sổ Feedback
        self.fb_screen = FeedbackWindow()  # Khởi tạo class FeedbackWindow bạn đã viết
        self.fb_screen.show()



class SelfCustomWindow(QMainWindow):
    def __init__(self, parent_logic):
        super().__init__()
        self.ui = Ui_SelfCustomWindow()
        self.ui.setupUi(self)
        self.parent_logic = parent_logic  # Lưu tham chiếu để gửi dữ liệu về

        # Kết nối nút xác nhận trong cửa sổ custom
        self.ui.buychocolatebalance_45.clicked.connect(self.confirm_custom)

    def confirm_custom(self):
        style = self.ui.chooseTheStyleComboBox.currentText()
        length = self.ui.chooseTheStyleComboBox_2.currentText()
        color = self.ui.txtSelectedColor.text()

        item_desc = f"Custom: {style}, {length}, {color}"
        self.parent_logic.add_to_cart(item_desc, 50.00)  # Gửi dữ liệu về bảng ở trang chính
        self.close()



class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.total_money = 0




    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # 1. Thiết lập Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(self.centralwidget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        MainWindow.setCentralWidget(scroll)

        # 2. Cài đặt ban đầu cho giỏ hàng

        self.labelTB_2.setText("0.00$")  # Khởi tạo giá trị ban đầu là 0

        # 3. Kết nối các nút chức năng chính
        self.pushButton_TB_9.clicked.connect(self.open_payment)  # Check out
        self.pushButton_TB_10.clicked.connect(self.remove_from_cart)  # Remove item
        self.buychocolatebalance_79.clicked.connect(self.open_self_custom)# Call staff
        self.menuMore_about_us.aboutToShow.connect(self.show_about_us)#mo ta


        self.buychocolatebalance_39.clicked.connect(lambda: self.add_to_cart("Chocolate Balance", 36))
        self.buychocolatebalance_40.clicked.connect(lambda: self.add_to_cart("Milk Chocolate", 36))
        self.buychocolatebalance_41.clicked.connect(lambda: self.add_to_cart("Dark Chocolate", 36))
        self.buychocolatebalance_42.clicked.connect(lambda: self.add_to_cart("Spring Special", 36))
        self.buychocolatebalance_44.clicked.connect(lambda: self.add_to_cart("Summer Nail", 36))

    def add_to_cart(self, item_name, price):
        """Thêm sản phẩm và cập nhật tổng tiền ngay lập tức"""
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        self.tableWidget.setItem(row_count, 0, QTableWidgetItem(item_name))
        self.tableWidget.setItem(row_count, 1, QTableWidgetItem("1"))
        self.tableWidget.setItem(row_count, 2, QTableWidgetItem(f"{price}$"))

        self.total_money += price
        self.labelTB_2.setText(f"{self.total_money:.2f}$")

    def remove_from_cart(self):
        """Xóa hàng đang được chọn trong bảng và trừ tiền tương ứng"""
        current_row = self.tableWidget.currentRow()

        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Warning", "Please select an item to remove!")
            return

        # Lấy giá tiền của hàng sắp xóa để trừ vào tổng
        price_item = self.tableWidget.item(current_row, 2)
        if price_item:
            price_val = float(price_item.text().replace('$', ''))
            self.total_money -= price_val

        # Xóa hàng và cập nhật lại hiển thị
        self.tableWidget.removeRow(current_row)
        self.labelTB_2.setText(f"{max(0, self.total_money):.2f}$")

    def open_payment(self):
        if self.total_money <= 0:
            QMessageBox.warning(self.MainWindow, "Empty", "Your cart is empty!")
            return


        self.payment_screen = PaymentWindow(self.labelTB_2.text())
        self.payment_screen.show()


    def show(self):
        self.MainWindow.show()

    def open_self_custom(self):
        self.custom_screen = SelfCustomWindow(self)
        self.custom_screen.show()

    def show_about_us(self):

        about_title = "✨ ABOUT MY NAIL SHOP ✨"


        about_text = (
            "<b>Vision:</b> <i>'Elevating Vietnamese Beauty Through Every Stroke'</i><br><br>"
            "<b>Our Professional Team:</b><br>"
            "• All technicians are <b>extensively trained</b> and certified by industry experts.<br>"
            "• We stay ahead of the curve with the <b>latest global nail trends</b>.<br>"
            "• Dedicated to providing meticulous service with <b>unmatched attention to detail</b>.<br><br>"
            "<b>Our Commitment:</b><br>"
            "• <b>100% Customer Satisfaction Guarantee</b>: Your happiness is our priority.<br>"
            "• <b>Premium Quality</b>: We use only high-end, non-toxic, and eco-friendly products.<br>"
            "• <b>Standard Hygiene</b>: A 5-star relaxing environment with sterilized equipment.<br><br>"
            "<b>Contact Information:</b><br>"
            "📍 Address: UEL University Village, Di An, Binh Duong.<br>"
            "📞 Hotline: (+84) 123 456 789<br>"
            "⏰ Hours: 08:00 AM - 09:00 PM (Daily)"
        )

        # Tạo một QMessageBox tùy chỉnh để điều chỉnh kích thước
        msg = QtWidgets.QMessageBox(self.MainWindow)
        msg.setWindowTitle("About Our Services")
        msg.setTextFormat(QtCore.Qt.TextFormat.RichText)  # Cho phép dùng thẻ HTML (b, i, br) để nội dung đẹp hơn
        msg.setText(about_title)
        msg.setInformativeText(about_text)
        msg.setStyleSheet("QLabel{ min-width: 500px; font-size: 13px; }")
        msg.exec()
