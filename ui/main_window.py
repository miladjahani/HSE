"""
ui/main_window.py
پنجره اصلی برنامه: سایدبار ثابت در سمت راست + ناحیه محتوای صفحات (QStackedWidget).
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt

from core.config import COLORS, APP_NAME
from ui.widgets.sidebar import Sidebar
from ui.dashboard import DashboardPage
from ui.personnel import PersonnelPage
from ui.incidents import IncidentsPage
from ui.ppe import PpeStockPage, PpeIssuancePage
from ui.training import TrainingPage
from ui.medical import MedicalPage
from ui.disciplinary import DisciplinaryPage
from ui.reports import ReportsPage
from ui.backup import BackupPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1280, 800)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(f"background-color: {COLORS['bg_main']};")

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setCentralWidget(central)

        self.sidebar = Sidebar()
        self.sidebar.navigate.connect(self._navigate)
        layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 1)

        # ترتیب باید دقیقاً با کلیدهای MENU_ITEMS در sidebar.py هماهنگ باشد
        self.pages = {}
        self._register_page("dashboard", DashboardPage())
        self._register_page("personnel", PersonnelPage())
        self._register_page("incidents", IncidentsPage())
        self._register_page("ppe_stock", PpeStockPage())
        self._register_page("ppe_issuance", PpeIssuancePage())
        self._register_page("training", TrainingPage())
        self._register_page("medical", MedicalPage())
        self._register_page("disciplinary", DisciplinaryPage())
        self._register_page("reports", ReportsPage())
        self._register_page("backup", BackupPage())

        self._navigate("dashboard")

    def _register_page(self, key, widget):
        self.pages[key] = widget
        self.stack.addWidget(widget)

    def _navigate(self, key):
        self.sidebar.set_active(key)
        widget = self.pages.get(key)
        if widget is None:
            return
        self.stack.setCurrentWidget(widget)
        if hasattr(widget, "reload"):
            widget.reload()
