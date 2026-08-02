"""
ui/disciplinary.py
ماژول تشویق و تنبیه پرسنل.
"""
from ui.widgets.crud_page import CrudPage

FIELDS = [
    {"key": "personnel_id", "label": "پرسنل", "type": "personnel_lookup", "required": True},
    {"key": "record_type", "label": "نوع", "type": "combo", "options": ["تشویق", "تنبیه"]},
    {"key": "title", "label": "عنوان", "type": "text"},
    {"key": "description", "label": "شرح", "type": "textarea"},
    {"key": "event_date_shamsi", "label": "تاریخ وقوع", "type": "date", "required": True},
    {"key": "reward_or_penalty", "label": "نوع پاداش/جریمه", "type": "text"},
    {"key": "registered_by", "label": "ثبت‌کننده", "type": "text"},
]
LIST_COLUMNS = ["personnel_id", "record_type", "title", "event_date_shamsi", "reward_or_penalty"]


class DisciplinaryPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="disciplinary_records",
            title="مدیریت تشویق‌ها و تنبیهات",
            fields=FIELDS,
            list_columns=LIST_COLUMNS,
            parent=parent,
        )
