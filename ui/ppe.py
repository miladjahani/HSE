"""
ui/ppe.py
ماژول تجهیزات حفاظت فردی: تعریف انبار (کالا/موجودی) و ثبت تحویل به پرسنل.
هشدار انقضا و کمبود موجودی در همین صفحات با رنگ‌آمیزی نمایش داده می‌شود.
"""
from PySide6.QtWidgets import QLabel
from ui.widgets.crud_page import CrudPage
from core.config import COLORS
from core.date_utils import days_between

STOCK_FIELDS = [
    {"key": "item_name", "label": "نام کالا", "type": "text", "required": True},
    {"key": "item_code", "label": "کد کالا", "type": "text"},
    {"key": "unit", "label": "واحد", "type": "text"},
    {"key": "stock_qty", "label": "موجودی فعلی", "type": "number"},
    {"key": "min_qty", "label": "حداقل موجودی (هشدار)", "type": "number"},
    {"key": "shelf_life_months", "label": "عمر مفید (ماه)", "type": "number"},
]
STOCK_LIST_COLUMNS = ["item_name", "item_code", "unit", "stock_qty", "min_qty"]


class PpeStockPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="ppe_items",
            title="انبار تجهیزات حفاظت فردی (PPE)",
            fields=STOCK_FIELDS,
            list_columns=STOCK_LIST_COLUMNS,
            parent=parent,
        )
        note = QLabel("توجه: ردیف‌هایی که موجودی آن‌ها کمتر از حداقل تعریف‌شده باشد، باید تامین شوند.")
        note.setStyleSheet(f"color: {COLORS['safety_orange']}; font-size: 11px;")
        self.layout().addWidget(note)


ISSUANCE_FIELDS = [
    {"key": "personnel_id", "label": "پرسنل", "type": "personnel_lookup", "required": True},
    {"key": "ppe_item_id", "label": "کالا (شناسه)", "type": "number", "required": True},
    {"key": "qty", "label": "تعداد", "type": "number"},
    {"key": "issue_date_shamsi", "label": "تاریخ تحویل", "type": "date", "required": True},
    {"key": "expiry_date_shamsi", "label": "تاریخ انقضا", "type": "date"},
    {"key": "notes", "label": "توضیحات", "type": "text"},
]
ISSUANCE_LIST_COLUMNS = ["personnel_id", "ppe_item_id", "qty", "issue_date_shamsi", "expiry_date_shamsi"]


class PpeIssuancePage(CrudPage):
    """
    نکته: فیلد 'کالا (شناسه)' عمداً به شکل عدد ساده نگه داشته شده تا کاربر شناسه
    ردیف کالا را از صفحه «انبار PPE» وارد کند. در نسخه‌های بعدی می‌توان آن را نیز
    به personnel_lookup مانند یک Combo اختصاصی برای کالاها تبدیل کرد.
    """
    def __init__(self, parent=None):
        super().__init__(
            table="ppe_issuance",
            title="تحویل تجهیزات حفاظت فردی به پرسنل",
            fields=ISSUANCE_FIELDS,
            list_columns=ISSUANCE_LIST_COLUMNS,
            parent=parent,
        )
        note = QLabel("هشدار انقضا: رکوردهایی که کمتر از ۳۰ روز به تاریخ انقضای آن‌ها مانده در گزارش‌ها مشخص می‌شوند.")
        note.setStyleSheet(f"color: {COLORS['safety_orange']}; font-size: 11px;")
        self.layout().addWidget(note)
