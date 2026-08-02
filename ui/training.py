"""
ui/training.py
ماژول آموزش: تعریف دوره‌های آموزشی و ثبت شرکت پرسنل در هر دوره
با هشدار سررسید تمدید بر اساس اعتبار دوره.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.widgets.crud_page import CrudPage
from core.config import COLORS

COURSE_FIELDS = [
    {"key": "course_title", "label": "عنوان دوره", "type": "text", "required": True},
    {"key": "validity_months", "label": "اعتبار (ماه)", "type": "number"},
]
COURSE_LIST_COLUMNS = ["course_title", "validity_months"]


class TrainingCoursesPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="training_courses",
            title="تعریف دوره‌های آموزشی",
            fields=COURSE_FIELDS,
            list_columns=COURSE_LIST_COLUMNS,
            parent=parent,
        )


RECORD_FIELDS = [
    {"key": "personnel_id", "label": "پرسنل", "type": "personnel_lookup", "required": True},
    {"key": "course_id", "label": "شناسه دوره", "type": "number", "required": True},
    {"key": "completion_date_shamsi", "label": "تاریخ گذراندن دوره", "type": "date", "required": True},
    {"key": "expiry_date_shamsi", "label": "تاریخ سررسید تمدید", "type": "date"},
    {"key": "score", "label": "نمره/نتیجه", "type": "text"},
    {"key": "certificate_path", "label": "گواهینامه", "type": "file"},
]
RECORD_LIST_COLUMNS = ["personnel_id", "course_id", "completion_date_shamsi", "expiry_date_shamsi"]


class TrainingRecordsPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="training_records",
            title="ثبت شرکت پرسنل در دوره‌های آموزشی",
            fields=RECORD_FIELDS,
            list_columns=RECORD_LIST_COLUMNS,
            parent=parent,
        )


class TrainingPage(QWidget):
    """صفحه ترکیبی تب‌دار: تعریف دوره‌ها + ثبت شرکت پرسنل در دوره‌ها."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: none; }}
            QTabBar::tab {{
                background: {COLORS['bg_panel']};
                color: {COLORS['text_secondary']};
                padding: 10px 18px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background: {COLORS['bg_card']};
                color: {COLORS['accent']};
                font-weight: bold;
            }}
        """)
        self.courses_page = TrainingCoursesPage()
        self.records_page = TrainingRecordsPage()
        tabs.addTab(self.courses_page, "دوره‌های آموزشی")
        tabs.addTab(self.records_page, "ثبت شرکت پرسنل")
        layout.addWidget(tabs)

    def reload(self):
        self.courses_page.reload()
        self.records_page.reload()
