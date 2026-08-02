from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QFrame, QFormLayout
)
from PySide6.QtCore import Qt

from core.config import COLORS
from core.database import db

class PersonnelProfilePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        header = QLabel("پرونده جامع پرسنل")
        header.setStyleSheet(f"color: {{COLORS['text_primary']}}; font-size: 18px; font-weight: bold;")
        root.addWidget(header)

        # Selection bar
        selection_layout = QHBoxLayout()
        selection_label = QLabel("انتخاب پرسنل (نام یا کد):")
        selection_label.setStyleSheet(f"color: {{COLORS['text_secondary']}};")
        self.personnel_combo = QComboBox()
        self.personnel_combo.setEditable(True)
        self.personnel_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {{COLORS['bg_input']}};
                color: {{COLORS['text_primary']}};
                border: 1px solid {{COLORS['border']}};
                border-radius: 6px;
                padding: 6px 8px;
            }}
        """)
        self.personnel_combo.currentIndexChanged.connect(self._on_personnel_selected)

        selection_layout.addWidget(selection_label)
        selection_layout.addWidget(self.personnel_combo, 1)
        root.addLayout(selection_layout)

        # Scroll area for the details
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: transparent; }}")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 10, 0)
        content_layout.setSpacing(20)

        # 1. Info Frame
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet(f"background-color: {{COLORS['bg_card']}}; border-radius: 8px;")
        info_layout = QFormLayout(self.info_frame)
        self.info_labels = {}
        info_fields = [
            ("personnel_code", "کد پرسنلی"),
            ("national_id", "کد ملی"),
            ("position", "سمت"),
            ("department", "بخش"),
            ("contract_status", "وضعیت قرارداد"),
            ("ppe_size", "سایز PPE")
        ]
        for key, label in info_fields:
            val_label = QLabel("-")
            val_label.setStyleSheet(f"color: {{COLORS['text_primary']}};")
            lbl = QLabel(label + ":")
            lbl.setStyleSheet(f"color: {{COLORS['text_secondary']}};")
            info_layout.addRow(lbl, val_label)
            self.info_labels[key] = val_label

        content_layout.addWidget(self.info_frame)

        # Helper to create tables
        def make_table(title, columns):
            layout = QVBoxLayout()
            lbl = QLabel(title)
            lbl.setStyleSheet(f"color: {{COLORS['accent']}}; font-weight: bold; margin-top: 10px;")
            layout.addWidget(lbl)

            table = QTableWidget()
            table.setColumnCount(len(columns))
            table.setHorizontalHeaderLabels(columns)
            table.horizontalHeader().setStretchLastSection(True)
            table.setStyleSheet(f"""
                QTableWidget {{
                    background-color: {{COLORS['bg_card']}};
                    color: {{COLORS['text_primary']}};
                    border: 1px solid {{COLORS['border']}};
                    border-radius: 6px;
                }}
                QHeaderView::section {{
                    background-color: {{COLORS['bg_panel']}};
                    color: {{COLORS['text_secondary']}};
                    border: none;
                    border-bottom: 1px solid {{COLORS['border']}};
                    padding: 4px;
                }}
            """)
            layout.addWidget(table)
            content_layout.addLayout(layout)
            return table

        # Tables
        self.ppe_table = make_table("تحویل PPE", ["کالا", "تعداد", "تاریخ تحویل", "تاریخ انقضا"])
        self.incidents_table = make_table("حوادث و شبه‌حوادث", ["تاریخ", "نوع", "شدت", "وضعیت"])
        self.medical_table = make_table("معاینات طب کار", ["نوع معاینه", "تاریخ", "تاریخ بعدی", "نتیجه"])
        self.training_table = make_table("آموزش", ["دوره", "تاریخ اتمام", "اعتبار"])
        self.disciplinary_table = make_table("تشویق و تنبیه", ["تاریخ", "نوع", "عنوان", "توضیحات"])

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        root.addWidget(scroll, 1)

    def reload(self):
        self.personnel_combo.blockSignals(True)
        self.personnel_combo.clear()
        self.personnel_combo.addItem("--- انتخاب کنید ---", None)
        rows = db.fetch_all("SELECT id, personnel_code, first_name, last_name FROM personnel ORDER BY last_name, first_name")
        for r in rows:
            self.personnel_combo.addItem(f"{r['first_name']} {r['last_name']} ({r['personnel_code']})", r["id"])
        self.personnel_combo.blockSignals(False)
        self._clear_data()

    def _clear_data(self):
        for lbl in self.info_labels.values():
            lbl.setText("-")
        for t in [self.ppe_table, self.incidents_table, self.medical_table, self.training_table, self.disciplinary_table]:
            t.setRowCount(0)

    def _on_personnel_selected(self, index):
        if index <= 0:
            self._clear_data()
            return

        pid = self.personnel_combo.currentData()
        if not pid:
            return

        self._load_personnel_data(pid)

    def _load_personnel_data(self, pid):
        # Info
        p = db.fetch_one("SELECT * FROM personnel WHERE id=?", (pid,))
        if p:
            for key, lbl in self.info_labels.items():
                lbl.setText(str(p.get(key) or "-"))

        # PPE
        ppe_rows = db.fetch_all('''
            SELECT p.item_name, i.qty, i.issue_date_shamsi, i.expiry_date_shamsi
            FROM ppe_issuance i
            JOIN ppe_items p ON i.ppe_item_id = p.id
            WHERE i.personnel_id=?
            ORDER BY i.issue_date_shamsi DESC
        ''', (pid,))
        self._fill_table(self.ppe_table, ppe_rows, ["item_name", "qty", "issue_date_shamsi", "expiry_date_shamsi"])

        # Incidents
        inc_rows = db.fetch_all('''
            SELECT incident_date_shamsi, incident_type, severity, action_status
            FROM incidents WHERE personnel_id=?
            ORDER BY incident_date_shamsi DESC
        ''', (pid,))
        self._fill_table(self.incidents_table, inc_rows, ["incident_date_shamsi", "incident_type", "severity", "action_status"])

        # Medical
        med_rows = db.fetch_all('''
            SELECT exam_type, exam_date_shamsi, next_due_date_shamsi, result
            FROM medical_exams WHERE personnel_id=?
            ORDER BY exam_date_shamsi DESC
        ''', (pid,))
        self._fill_table(self.medical_table, med_rows, ["exam_type", "exam_date_shamsi", "next_due_date_shamsi", "result"])

        # Training
        trn_rows = db.fetch_all('''
            SELECT c.course_title, r.completion_date_shamsi, r.expiry_date_shamsi
            FROM training_records r
            JOIN training_courses c ON r.course_id = c.id
            WHERE r.personnel_id=?
            ORDER BY r.completion_date_shamsi DESC
        ''', (pid,))
        self._fill_table(self.training_table, trn_rows, ["course_title", "completion_date_shamsi", "expiry_date_shamsi"])

        # Disciplinary
        disc_rows = db.fetch_all('''
            SELECT event_date_shamsi, record_type, title, description
            FROM disciplinary_records WHERE personnel_id=?
            ORDER BY event_date_shamsi DESC
        ''', (pid,))
        self._fill_table(self.disciplinary_table, disc_rows, ["event_date_shamsi", "record_type", "title", "description"])

    def _fill_table(self, table, rows, cols):
        table.setRowCount(len(rows))
        for r_idx, row in enumerate(rows):
            for c_idx, col in enumerate(cols):
                val = row[col] if col in row.keys() else ""
                item = QTableWidgetItem(str(val or ""))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                table.setItem(r_idx, c_idx, item)
