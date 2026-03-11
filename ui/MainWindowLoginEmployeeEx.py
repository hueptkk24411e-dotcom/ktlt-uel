import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from libs.DataConnector import DataConnector
from ui.MainWindowEx import MainWindowEx
from ui.MainWindowLogin import Ui_MainWindow
class MainWindowLoginEx(QMainWindow):
    MAX_ATTEMPTS = 3  # Số lần nhập sai tối đa
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonLogin.clicked.connect(self.process_login)
        self.ui.pushButtonExit.clicked.connect(self.process_exit)
        # Khởi tạo DataConnector để đọc dữ liệu từ JSON
        self.data_connector = DataConnector("../datasets/employees.json")

        # Biến đếm số lần nhập sai
        self.login_attempts = 0

    def process_login(self):
        username = self.ui.lineEditUsername.text().strip()
        password = self.ui.lineEditPassword.text().strip()


        # kiểm tra login từ JSON
        employee = self.data_connector.validate_employee_login(username, password)

        if employee:
            self.open_main_window(employee["EmployeeId"])
        else:
            self.login_attempts += 1

            if self.login_attempts >= self.MAX_ATTEMPTS:
                self.show_exit_warning()
            else:
                self.show_login_failed_message()

    def open_main_window(self, employee_name):
        self.main_window = QMainWindow()
        self.main_ui = MainWindowEx()
        self.main_ui.setupUi(self.main_window)

        self.main_ui.show()  # sửa dòng này

        self.close()


    def show_login_failed_message(self):
        """Hiển thị thông báo lỗi khi đăng nhập sai"""
        QMessageBox.warning(self, "Đăng nhập thất bại", f"Sai tài khoản hoặc mật khẩu!\n(Lần thử {self.login_attempts}/{self.MAX_ATTEMPTS})")

    def show_exit_warning(self):
        """Cảnh báo khi nhập sai quá nhiều lần và đóng ứng dụng"""
        QMessageBox.critical(self, "Quá số lần thử", "Bạn đã nhập sai quá 3 lần!\nChương trình sẽ tự động thoát.")
        self.close()  # Đóng cửa sổ
        sys.exit()  # Thoát hoàn toàn ứng dụng

    def process_exit(self):
        """Thoát chương trình khi bấm nút Exit"""
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowLoginEx()
    window.show()
    sys.exit(app.exec())