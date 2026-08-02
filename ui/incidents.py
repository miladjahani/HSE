"""
ui/incidents.py
ماژول مدیریت حوادث و شبه‌حوادث.
"""
from ui.widgets.crud_page import CrudPage

FIELDS = [
    {"key": "incident_date_shamsi", "label": "تاریخ وقوع", "type": "date", "required": True},
    {"key": "incident_time", "label": "ساعت وقوع", "type": "text"},
    {"key": "location", "label": "مکان", "type": "text"},
    {"key": "incident_type", "label": "نوع", "type": "combo",
     "options": ["حادثه", "شبه‌حادثه", "نزدیک به حادثه"]},
    {"key": "severity", "label": "شدت", "type": "combo",
     "options": ["جزئی", "متوسط", "شدید", "فوت"]},
    {"key": "personnel_id", "label": "فرد درگیر (در صورت وجود)", "type": "personnel_lookup"},
    {"key": "description", "label": "شرح حادثه", "type": "textarea"},
    {"key": "root_cause", "label": "علل ریشه‌ای", "type": "textarea"},
    {"key": "corrective_action", "label": "اقدامات اصلاحی", "type": "textarea"},
    {"key": "action_status", "label": "وضعیت اقدام", "type": "combo",
     "options": ["باز", "در حال انجام", "بسته"]},
    {"key": "attachment_path", "label": "پیوست عکس/مدرک", "type": "file"},
]

LIST_COLUMNS = ["incident_date_shamsi", "incident_type", "severity", "location", "action_status"]


class IncidentsPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="incidents",
            title="مدیریت حوادث و شبه‌حوادث",
            fields=FIELDS,
            list_columns=LIST_COLUMNS,
            parent=parent,
        )
