"""
ui/reports.py
گزارش‌گیری و تولید خروجی Excel/CSV از تمام جداول دیتابیس.
"""
import os
import csv

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox, QFileDialog
)

from core.config import COLORS, EXPORT_DIR
from core.database import db

TABLES = {
    "personnel": "پرسنل",
    "incidents": "حوادث و شبه‌حوادث",
    "ppe_items": "انبار PPE",
    "ppe_issuance": "تحویل PPE",
    "training_courses": "دوره‌های آموزشی",
    "training_records": "ثبت دوره‌های آموزشی",
    "medical_exams": "معاینات طب کار",
    "disciplinary_records": "تشویق و تنبیه",
}


class ReportsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        header = QLabel("گزارش‌گیری و خروجی داده‌ها")
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        root.addWidget(header)

        desc = QLabel("یک یا چند جدول را انتخاب کرده و فرمت خروجی را مشخص کنید.")
        desc.setStyleSheet(f"color: {COLORS['text_secondary']};")
        root.addWidget(desc)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 6px;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['accent']};
                color: #1B2129;
            }}
        """)
        for key, label in TABLES.items():
            item = QListWidgetItem(label)
            item.setData(1000, key)
            self.list_widget.addItem(item)
        root.addWidget(self.list_widget, 1)

        btn_row = QHBoxLayout()
        excel_btn = QPushButton("خروجی Excel (.xlsx)")
        csv_btn = QPushButton("خروجی CSV")
        for b, color in [(excel_btn, COLORS["accent"]), (csv_btn, COLORS["safety_blue"])]:
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #1B2129;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 16px;
                    font-weight: bold;
                }}
            """)
        excel_btn.clicked.connect(self._export_excel)
        csv_btn.clicked.connect(self._export_csv)
        btn_row.addWidget(excel_btn)
        btn_row.addWidget(csv_btn)
        root.addLayout(btn_row)

    def _selected_tables(self):
        return [item.data(1000) for item in self.list_widget.selectedItems()]

    def _export_csv(self):
        tables = self._selected_tables()
        if not tables:
            QMessageBox.warning(self, "خطا", "حداقل یک جدول را انتخاب کنید.")
            return
        folder = QFileDialog.getExistingDirectory(self, "انتخاب پوشه ذخیره‌سازی", EXPORT_DIR)
        if not folder:
            return
        for t in tables:
            rows = db.fetch_all(f"SELECT * FROM {t}")
            path = os.path.join(folder, f"{t}.csv")
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                if rows:
                    writer.writerow(rows[0].keys())
                    for r in rows:
                        writer.writerow(list(r))
                else:
                    writer.writerow(["(بدون داده)"])
        QMessageBox.information(self, "موفق", f"فایل‌های CSV در مسیر زیر ذخیره شدند:\n{folder}")

    def _export_excel(self):
        try:
            import openpyxl
            from openpyxl.styles import Font
        except ImportError:
            QMessageBox.critical(
                self, "خطا",
                "کتابخانه openpyxl نصب نیست. دستور نصب:\npip install openpyxl"
            )
            return

        tables = self._selected_tables()
        if not tables:
            QMessageBox.warning(self, "خطا", "حداقل یک جدول را انتخاب کنید.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "ذخیره فایل اکسل", os.path.join(EXPORT_DIR, "hse_report.xlsx"), "Excel Files (*.xlsx)"
        )
        if not path:
            return

        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        for t in tables:
            rows = db.fetch_all(f"SELECT * FROM {t}")
            ws = wb.create_sheet(title=TABLES.get(t, t)[:31])
            if rows:
                ws.append(list(rows[0].keys()))
                for cell in ws[1]:
                    cell.font = Font(bold=True)
                for r in rows:
                    ws.append(list(r))
            else:
                ws.append(["(بدون داده)"])
        wb.save(path)
        QMessageBox.information(self, "موفق", f"فایل اکسل ذخیره شد:\n{path}")
