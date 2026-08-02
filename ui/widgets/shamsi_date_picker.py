"""
ui/widgets/shamsi_date_picker.py
یک Date Picker گرافیکی شمسی سبک و زیبا، سازگار با تم تیره صنعتی.
به صورت QLineEdit + دکمه تقویم پیاده شده که با کلیک، یک Popup تقویمی باز می‌شود.
"""
import jdatetime
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QToolButton, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from core.config import COLORS, JALALI_MONTHS, WEEKDAYS_FA
from core.date_utils import is_valid_shamsi_date, shamsi_today_ymd


class _CalendarPopup(QFrame):
    date_selected = Signal(str)

    def __init__(self, parent=None, year=None, month=None):
        super().__init__(parent, Qt.Popup)
        y, m, _ = shamsi_today_ymd()
        self.year = year or y
        self.month = month or m
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
            QLabel {{ color: {COLORS['text_primary']}; }}
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 6px;
                padding: 6px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent']};
                color: #1B2129;
            }}
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # هدر: ناوبری ماه
        header = QHBoxLayout()
        prev_btn = QPushButton("<")
        next_btn = QPushButton(">")
        prev_btn.setFixedWidth(30)
        next_btn.setFixedWidth(30)
        prev_btn.clicked.connect(self._prev_month)
        next_btn.clicked.connect(self._next_month)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"font-weight: bold; color: {COLORS['accent']};")

        header.addWidget(next_btn)
        header.addWidget(self.title_label, 1)
        header.addWidget(prev_btn)
        layout.addLayout(header)

        # روزهای هفته
        wd_layout = QHBoxLayout()
        for wd in WEEKDAYS_FA:
            lbl = QLabel(wd[:1])
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
            wd_layout.addWidget(lbl)
        layout.addLayout(wd_layout)

        self.grid = QGridLayout()
        self.grid.setSpacing(4)
        layout.addLayout(self.grid)

        self._render_days()

    def _month_len(self, year, month):
        return 31 if month <= 6 else (30 if month <= 11 else (30 if jdatetime.date(year, 1, 1).isleap() else 29))

    def _render_days(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.title_label.setText(f"{JALALI_MONTHS[self.month - 1]}   {self.year}")

        first_day = jdatetime.date(self.year, self.month, 1)
        start_col = (first_day.weekday() + 1) % 7  # شنبه = ستون 0 در تقویم ایرانی
        n_days = self._month_len(self.year, self.month)

        row, col = 0, start_col
        for day in range(1, n_days + 1):
            btn = QPushButton(str(day))
            btn.setFixedSize(32, 28)
            btn.clicked.connect(lambda _, d=day: self._pick(d))
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def _prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self._render_days()

    def _next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self._render_days()

    def _pick(self, day):
        value = f"{self.year:04d}/{self.month:02d}/{day:02d}"
        self.date_selected.emit(value)
        self.close()


class ShamsiDateEdit(QWidget):
    """کامپوننت انتخاب تاریخ شمسی؛ خروجی همیشه رشته‌ی 'YYYY/MM/DD' است."""
    date_changed = Signal(str)

    def __init__(self, parent=None, default_today=True):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("1403/01/01")
        self.line_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 6px 8px;
            }}
        """)

        self.calendar_btn = QToolButton()
        self.calendar_btn.setText("📅")
        self.calendar_btn.setStyleSheet(f"""
            QToolButton {{
                background-color: {COLORS['bg_input']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px 8px;
                color: {COLORS['accent']};
            }}
            QToolButton:hover {{ border-color: {COLORS['accent']}; }}
        """)
        self.calendar_btn.clicked.connect(self._open_calendar)

        layout.addWidget(self.line_edit, 1)
        layout.addWidget(self.calendar_btn)

        if default_today:
            y, m, d = shamsi_today_ymd()
            self.set_value(f"{y:04d}/{m:02d}/{d:02d}")

    def _open_calendar(self):
        y, m, _ = shamsi_today_ymd()
        if is_valid_shamsi_date(self.line_edit.text()):
            y, m, _ = [int(x) for x in self.line_edit.text().split("/")]
        popup = _CalendarPopup(self, year=y, month=m)
        popup.date_selected.connect(self.set_value)
        pos = self.calendar_btn.mapToGlobal(self.calendar_btn.rect().bottomLeft())
        popup.move(pos)
        popup.show()

    def set_value(self, value: str):
        self.line_edit.setText(value)
        self.date_changed.emit(value)

    def value(self) -> str:
        return self.line_edit.text().strip()

    def is_valid(self) -> bool:
        return is_valid_shamsi_date(self.value())
