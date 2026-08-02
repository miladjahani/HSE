"""
ui/medical.py
ماژول طب کار: ثبت معاینات ادیومتری/اسپیرومتری/عمومی با هشدار سررسید.
"""
from ui.widgets.crud_page import CrudPage

FIELDS = [
    {"key": "personnel_id", "label": "پرسنل", "type": "personnel_lookup", "required": True},
    {"key": "exam_type", "label": "نوع معاینه", "type": "combo",
     "options": ["عمومی", "ادیومتری", "اسپیرومتری", "بینایی‌سنجی", "سایر"]},
    {"key": "exam_date_shamsi", "label": "تاریخ معاینه", "type": "date", "required": True},
    {"key": "next_due_date_shamsi", "label": "تاریخ سررسید بعدی", "type": "date"},
    {"key": "result", "label": "نتیجه", "type": "combo",
     "options": ["سالم", "نیازمند پیگیری", "محدودیت شغلی", "سایر"]},
    {"key": "notes", "label": "توضیحات", "type": "textarea"},
    {"key": "attachment_path", "label": "پیوست مدرک پزشکی", "type": "file"},
]
LIST_COLUMNS = ["personnel_id", "exam_type", "exam_date_shamsi", "next_due_date_shamsi", "result"]


class MedicalPage(CrudPage):
    def __init__(self, parent=None):
        super().__init__(
            table="medical_exams",
            title="طب کار و معاینات دوره‌ای",
            fields=FIELDS,
            list_columns=LIST_COLUMNS,
            parent=parent,
        )
