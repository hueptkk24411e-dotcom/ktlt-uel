import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.LoginWindowEx import LoginWindowEx

app = QApplication(sys.argv)
gui = LoginWindowEx()
win = QMainWindow()
gui.setupUi(win)
gui.showWindow()
sys.exit(app.exec())
