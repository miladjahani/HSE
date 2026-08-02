"""
ui/personnel.py
ماژول مدیریت پرسنل: ثبت مشخصات کامل، کد پرسنلی، سمت و وضعیت قرارداد.
"""
from ui.widgets.crud_page import CrudPage

FIELDS = [
    {"key": "personnel_code", "label": "کد پرسنلی", "type": "text", "required": True},
    {"key": "first_name", "label": "نام", "type": "text", "required": True},
    {"key": "last_name", "label": "نام خانوادگی", "type": "text", "required": True},
    {"key": "national_id", "label": "کد ملی", "type": "text"},
    {"key": "position", "label": "سمت", "type": "text"},
    {"key": "department", "label": "واحد / بخش", "type": "text"},
    {"key": "contract_type", "label": "نوع قرارداد", "type": "combo",
     "options": ["رسمی", "قراردادی", "پیمانکار", "کارآموز"]},
    {"key": "contract_status", "label": "وضعیت قرارداد", "type": "combo",
     "options": ["فعال", "تعلیق", "پایان‌یافته"]},
    {"key": "hire_date_shamsi", "label": "تاریخ استخدام", "type": "date"},
    {"key": "phone", "label": "شماره تماس", "type": "text"},
    {"key": "photo_path", "label": "تصویر پرسنلی", "type": "file"},
]

LIST_COLUMNS = ["personnel_code", "first_name", "last_name", "position", "contract_status"]


class PersonnelPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="personnel",
            title="مدیریت پرسنل",
            fields=FIELDS,
            list_columns=LIST_COLUMNS,
            parent=parent,
        )
