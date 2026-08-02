"""
ui/widgets/sidebar.py
منوی کناری ثابت با دکمه‌های بزرگ و آیکون‌دار، مناسب استفاده با دستکش.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

from core.config import COLORS, APP_NAME

MENU_ITEMS = [
    ("dashboard", "🏠", "داشبورد"),
    ("personnel", "👷", "پرسنل"),
    ("personnel_profile", "🗂", "پرونده جامع پرسنل"),
    ("incidents", "⚠️", "حوادث و شبه‌حوادث"),
    ("ppe_stock", "🦺", "انبار PPE"),
    ("ppe_issuance", "📦", "تحویل PPE"),
    ("training", "🎓", "دوره‌های آموزشی"),
    ("medical", "🩺", "طب کار"),
    ("disciplinary", "🏅", "تشویق و تنبیه"),
    ("reports", "📊", "گزارش‌گیری و خروجی"),
    ("backup", "💾", "پشتیبان‌گیری"),
]


class Sidebar(QWidget):
    navigate = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)
        self.setStyleSheet(f"background-color: {COLORS['sidebar']};")
        self._buttons = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        title = QLabel(APP_NAME)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            color: {COLORS['accent']};
            font-weight: bold;
            font-size: 13px;
            padding: 22px 12px;
            border-bottom: 1px solid {COLORS['border']};
        """)
        layout.addWidget(title)

        for key, icon, label in MENU_ITEMS:
            btn = QPushButton(f"  {icon}   {label}")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(48)
            btn.setStyleSheet(self._btn_style())
            btn.clicked.connect(lambda _, k=key: self._on_click(k))
            layout.addWidget(btn)
            self._buttons[key] = btn

        layout.addStretch(1)

    def _btn_style(self):
        return f"""
            QPushButton {{
                text-align: right;
                color: {COLORS['text_secondary']};
                background-color: transparent;
                border: none;
                border-right: 3px solid transparent;
                font-size: 13px;
                padding-right: 10px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_panel']};
                color: {COLORS['text_primary']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['bg_panel']};
                color: {COLORS['accent']};
                border-right: 3px solid {COLORS['accent']};
                font-weight: bold;
            }}
        """

    def set_active(self, key: str):
        for k, btn in self._buttons.items():
            btn.setChecked(k == key)

    def _on_click(self, key):
        self.set_active(key)
        self.navigate.emit(key)
