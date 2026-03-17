"""
SelfCustomWindowEx.py
──────────────────────
Import từ ui.constants — KHÔNG import COLOR_PALETTE từ SelfCustomWindow.py.
Sửa lỗi: COLOR_PALETTE và self._color_btns không tồn tại trong Ui_SelfCustomWindow,
          nay build dict nút màu trực tiếp từ getattr() + COLOR_PALETTE trong constants.
"""

from PyQt6.QtWidgets import QMainWindow

from nail_shop.nail_shop.ui.SelfCustomWindow import Ui_SelfCustomWindow
from nail_shop.nail_shop.ui.constants import COLOR_PALETTE

SELECTED_BORDER     = "3px solid #4A90E2"
DEFAULT_BORDER      = "1px solid #ddd"
DEFAULT_BORDER_WHITE = "2px solid #ccc"   # màu trắng dùng border đặc biệt


class SelfCustomWindowEx(Ui_SelfCustomWindow):
    def __init__(self, on_confirm_callback):
        self.on_confirm_callback = on_confirm_callback
        self.selected_color_hex  = None
        self.selected_color_name = None
        self._prev_btn           = None

    def setupUi(self, Window):
        super().setupUi(Window)
        self.Window = Window
        Window.setWindowTitle("Custom Your Design")

        # Build dict {object_name: btn} từ COLOR_PALETTE + getattr
        # Không cần _color_btns hay import gì thêm từ SelfCustomWindow
        self._color_btn_map = {}
        for obj_name, hex_color, color_name in COLOR_PALETTE:
            btn = getattr(self, obj_name, None)
            if btn is not None:
                self._color_btn_map[obj_name] = btn
                btn.clicked.connect(
                    lambda _, h=hex_color, n=color_name, b=btn:
                        self._on_color_click(h, n, b)
                )

        # Nút confirm
        self.buychocolatebalance_45.clicked.connect(self._confirm)

    def showWindow(self):
        self.Window.show()

    def _on_color_click(self, hex_color: str, name: str, btn):
        # Reset border nút trước đó
        if self._prev_btn and self._prev_btn is not btn:
            prev_hex = self._get_btn_hex(self._prev_btn)
            border = DEFAULT_BORDER_WHITE if prev_hex == "#FFFFFF" else DEFAULT_BORDER
            self._prev_btn.setStyleSheet(
                f"background-color: {prev_hex}; border-radius: 17px; border: {border};"
            )

        # Highlight nút được chọn
        btn.setStyleSheet(
            f"background-color: {hex_color}; border-radius: 17px;"
            f" border: {SELECTED_BORDER};"
        )
        self._prev_btn = btn

        # Cập nhật swatch và text
        self.lblColorSwatch.setStyleSheet(
            f"background-color: {hex_color}; border-radius: 15px;"
            f" border: 2px solid #AFCBF3;"
        )
        self.txtSelectedColor.setText(f"{name}  ({hex_color})")
        self.selected_color_hex  = hex_color
        self.selected_color_name = name

    def _get_btn_hex(self, btn) -> str:
        """Lấy màu hex từ stylesheet hiện tại của nút."""
        for obj_name, hex_color, _ in COLOR_PALETTE:
            if getattr(self, obj_name, None) is btn:
                return hex_color
        return "#FFFFFF"

    def _confirm(self):
        from PyQt6.QtWidgets import QMessageBox

        style  = self.chooseTheStyleComboBox.currentText().strip()
        length = self.chooseTheStyleComboBox_2.currentText().strip()
        color  = self.selected_color_name or "Not selected"
        note   = self.lineEditNote.text().strip()

        # Validate: item đầu là placeholder "..........."
        if style.startswith(".") or length.startswith("."):
            QMessageBox.warning(
                self.Window, "Incomplete",
                "Please select both a style and a length."
            )
            return

        desc = f"Custom: {style}, {length}, {color}"
        if note:
            desc += f" | {note[:50]}"

        self.on_confirm_callback(desc, 50.0)
        self.Window.close()
