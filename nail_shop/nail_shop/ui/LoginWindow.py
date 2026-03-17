from PyQt6 import QtCore, QtGui, QtWidgets

# Color palette from original project:
# BG_LIGHT  = rgb(234, 242, 251)
# HEADER    = rgb(167, 212, 238)
# ACCENT    = rgb(67, 139, 196)
# BORDER    = rgb(170, 210, 250)
# TEXT_DARK = rgb(0, 0, 127)
# BTN_TEXT  = rgb(224, 253, 255)

STYLE_MAIN_BG = "background-color: rgb(234, 242, 251);"

STYLE_HEADER = """
    background-color: rgb(167, 212, 238);
    border-radius: 16px;
    color: white;
"""

STYLE_BTN_PRIMARY = """
    QPushButton {
        background-color: rgb(67, 139, 196);
        color: rgb(224, 253, 255);
        border: 2px solid rgb(170, 210, 250);
        border-radius: 10px;
        font-size: 13px;
        font-weight: bold;
        padding: 6px 14px;
    }
    QPushButton:hover  { background-color: #4E86B5; }
    QPushButton:pressed{ background-color: #3a6f99; }
"""

STYLE_BTN_CUSTOMER = """
    QPushButton {
        background-color: rgb(167, 212, 238);
        color: rgb(0, 0, 127);
        border: 2px solid rgb(67, 139, 196);
        border-radius: 14px;
        font-size: 15px;
        font-weight: bold;
        padding: 10px;
    }
    QPushButton:hover  { background-color: #A6C8FF; }
    QPushButton:pressed{ background-color: #7FAFFF; }
"""

STYLE_BTN_MANAGER = """
    QPushButton {
        background-color: rgb(67, 139, 196);
        color: rgb(224, 253, 255);
        border: 2px solid rgb(170, 210, 250);
        border-radius: 14px;
        font-size: 15px;
        font-weight: bold;
        padding: 10px;
    }
    QPushButton:hover  { background-color: #4E86B5; }
    QPushButton:pressed{ background-color: #3a6f99; }
"""

STYLE_INPUT = """
    QLineEdit {
        border: 2px solid rgb(170, 210, 250);
        border-radius: 8px;
        padding: 4px 8px;
        background-color: rgb(243, 248, 253);
        color: rgb(0, 0, 127);
        font-size: 13px;
    }
    QLineEdit:focus { border: 2px solid rgb(67, 139, 196); }
"""

STYLE_GROUPBOX = """
    QGroupBox {
        border: 2px solid rgb(170, 210, 250);
        border-radius: 10px;
        margin-top: 14px;
        font-weight: bold;
        color: rgb(0, 0, 127);
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 4px;
    }
"""


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(460, 520)
        LoginWindow.setMinimumSize(460, 520)

        self.centralwidget = QtWidgets.QWidget(parent=LoginWindow)
        self.centralwidget.setStyleSheet(STYLE_MAIN_BG)

        root = QtWidgets.QVBoxLayout(self.centralwidget)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # ── Header ─────────────────────────────────────────────
        header = QtWidgets.QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet(STYLE_HEADER)
        h_lay = QtWidgets.QVBoxLayout(header)
        h_lay.setContentsMargins(0, 6, 0, 6)

        lbl_title = QtWidgets.QLabel("MY NAIL SHOP")
        lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(
            "font-size: 26px; font-weight: bold; font-family: Georgia, serif; color: white;"
        )
        lbl_sub = QtWidgets.QLabel("Where Your Beauty and Satisfaction Come First")
        lbl_sub.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl_sub.setStyleSheet("font-size: 11px; color: white;")

        h_lay.addWidget(lbl_title)
        h_lay.addWidget(lbl_sub)
        root.addWidget(header)

        # ── Role selection ──────────────────────────────────────
        lbl_role = QtWidgets.QLabel("Please select your role:")
        lbl_role.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl_role.setStyleSheet("font-size: 13px; color: rgb(0,0,127); font-weight: bold;")
        root.addWidget(lbl_role)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(16)

        self.btnCustomer = QtWidgets.QPushButton("👤  Customer\n(No Login Required)")
        self.btnCustomer.setFixedHeight(70)
        self.btnCustomer.setStyleSheet(STYLE_BTN_CUSTOMER)

        self.btnManagerLogin = QtWidgets.QPushButton("🔐  Manager\n(Login Required)")
        self.btnManagerLogin.setFixedHeight(70)
        self.btnManagerLogin.setStyleSheet(STYLE_BTN_MANAGER)

        btn_row.addWidget(self.btnCustomer)
        btn_row.addWidget(self.btnManagerLogin)
        root.addLayout(btn_row)

        # ── Divider ─────────────────────────────────────────────
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setStyleSheet("color: rgb(170, 210, 250);")
        root.addWidget(line)

        # ── Manager login panel (hidden by default) ─────────────
        self.groupLogin = QtWidgets.QGroupBox("Manager Login")
        self.groupLogin.setStyleSheet(STYLE_GROUPBOX)
        self.groupLogin.setVisible(False)
        g_lay = QtWidgets.QFormLayout(self.groupLogin)
        g_lay.setContentsMargins(16, 20, 16, 16)
        g_lay.setSpacing(12)

        self.lineEditUsername = QtWidgets.QLineEdit()
        self.lineEditUsername.setPlaceholderText("Enter username...")
        self.lineEditUsername.setStyleSheet(STYLE_INPUT)
        self.lineEditUsername.setFixedHeight(34)

        self.lineEditPassword = QtWidgets.QLineEdit()
        self.lineEditPassword.setPlaceholderText("Enter password...")
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEditPassword.setStyleSheet(STYLE_INPUT)
        self.lineEditPassword.setFixedHeight(34)

        lbl_u = QtWidgets.QLabel("Username:")
        lbl_u.setStyleSheet("color: rgb(0,0,127); font-weight: bold;")
        lbl_p = QtWidgets.QLabel("Password:")
        lbl_p.setStyleSheet("color: rgb(0,0,127); font-weight: bold;")

        g_lay.addRow(lbl_u, self.lineEditUsername)
        g_lay.addRow(lbl_p, self.lineEditPassword)

        btn_login_row = QtWidgets.QHBoxLayout()
        self.btnLogin = QtWidgets.QPushButton("Login")
        self.btnLogin.setFixedHeight(34)
        self.btnLogin.setStyleSheet(STYLE_BTN_PRIMARY)

        self.btnBack = QtWidgets.QPushButton("Back")
        self.btnBack.setFixedHeight(34)
        self.btnBack.setStyleSheet(STYLE_BTN_PRIMARY.replace(
            "rgb(67, 139, 196)", "rgb(167, 212, 238)"
        ).replace("rgb(224, 253, 255)", "rgb(0, 0, 127)"))

        btn_login_row.addWidget(self.btnLogin)
        btn_login_row.addWidget(self.btnBack)
        g_lay.addRow(btn_login_row)

        root.addWidget(self.groupLogin)

        # ── Exit button ─────────────────────────────────────────
        root.addStretch()
        self.btnExit = QtWidgets.QPushButton("Exit App")
        self.btnExit.setFixedHeight(34)
        self.btnExit.setStyleSheet(STYLE_BTN_PRIMARY)
        root.addWidget(self.btnExit)

        LoginWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle("My Nail Shop")
