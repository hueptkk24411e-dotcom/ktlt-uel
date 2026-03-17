import sys
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow

from nail_shop.nail_shop.models.managers import Managers
from nail_shop.nail_shop.ui.LoginWindow import Ui_LoginWindow


class LoginWindowEx(Ui_LoginWindow):
    def __init__(self):
        self.file_managers = "datasets/managers.json"
        self.lm = Managers()
        self.lm.import_json(self.file_managers)
        self.login_attempts = 0
        self.MAX_ATTEMPTS = 3

    def setupUi(self, LoginWindow):
        super().setupUi(LoginWindow)
        self.LoginWindow = LoginWindow
        self.btnCustomer.clicked.connect(self.open_customer_info)
        self.btnManagerLogin.clicked.connect(self.show_login_panel)
        self.btnBack.clicked.connect(self.hide_login_panel)
        self.btnLogin.clicked.connect(self.process_login)
        self.btnExit.clicked.connect(self.process_exit)
        # Allow Enter key to submit login
        self.lineEditPassword.returnPressed.connect(self.process_login)

    def showWindow(self):
        self.LoginWindow.show()

    # ── Show/hide manager login panel ─────────────────────────
    def show_login_panel(self):
        self.groupLogin.setVisible(True)
        self.btnCustomer.setEnabled(False)
        self.btnManagerLogin.setEnabled(False)
        self.lineEditUsername.setFocus()

    def hide_login_panel(self):
        self.groupLogin.setVisible(False)
        self.btnCustomer.setEnabled(True)
        self.btnManagerLogin.setEnabled(True)
        self.lineEditUsername.clear()
        self.lineEditPassword.clear()
        self.login_attempts = 0

    # ── Customer: no login, open info form ────────────────────
    def open_customer_info(self):
        from ui.CustomerInfoWindowEx import CustomerInfoWindowEx
        self.cus_info_win = QMainWindow()
        self.cus_info_ex = CustomerInfoWindowEx(self)
        self.cus_info_ex.setupUi(self.cus_info_win)
        self.cus_info_ex.showWindow()

    # ── Manager login ─────────────────────────────────────────
    def process_login(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text().strip()

        manager = self.lm.find_by_username(username)

        if manager is None or manager.password != password:
            self.login_attempts += 1
            remaining = self.MAX_ATTEMPTS - self.login_attempts
            if self.login_attempts >= self.MAX_ATTEMPTS:
                QMessageBox.critical(
                    self.LoginWindow, "Locked",
                    "Too many failed attempts.\nApplication will close."
                )
                QApplication.quit()
            else:
                QMessageBox.warning(
                    self.LoginWindow, "Login Failed",
                    f"Invalid username or password.\nAttempts remaining: {remaining}"
                )
            return

        self.open_manager_window(manager)

    def open_manager_window(self, manager):
        from ui.ProductMainWindowEx import ProductMainWindowEx
        self.mgr_win = QMainWindow()
        self.mgr_ex = ProductMainWindowEx(self)
        self.mgr_ex.setupUi(self.mgr_win)
        self.mgr_ex.showWindow()
        self.LoginWindow.hide()

    # ── Exit ──────────────────────────────────────────────────
    def process_exit(self):
        reply = QMessageBox.question(
            self.LoginWindow, "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()
