from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.ProductMainWindowEx import ProductMainWindowEx

app=QApplication([])
gui=ProductMainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()