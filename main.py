"""
main.py
نقطه ورود برنامه. در اولین اجرا SetupWizard نمایش داده می‌شود، سپس MainWindow.
"""
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

from core.config import COLORS, FONT_FAMILY, FONT_SIZE_BASE, LOGO_PATH
from core.database import db
from ui.setup_wizard import SetupWizard
from ui.main_window import MainWindow


GLOBAL_STYLESHEET = f"""
QWidget {{
    font-family: "{FONT_FAMILY}", "Tahoma", sans-serif;
    font-size: {FONT_SIZE_BASE}pt;
}}
QToolTip {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
}}
QMessageBox {{
    background-color: {COLORS['bg_main']};
}}
QMessageBox QLabel {{
    color: {COLORS['text_primary']};
}}
QScrollBar:vertical {{
    background: {COLORS['bg_panel']};
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border']};
    border-radius: 5px;
}}
"""


def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    app.setStyleSheet(GLOBAL_STYLESHEET)
    app.setFont(QFont(FONT_FAMILY, FONT_SIZE_BASE))

    if not db.is_setup_completed():
        wizard = SetupWizard()
        if wizard.exec() != wizard.Accepted:
            sys.exit(0)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
