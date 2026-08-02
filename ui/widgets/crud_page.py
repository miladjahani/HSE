"""
ui/widgets/crud_page.py
یک صفحه عمومی «لیست + فرم» که با یک تعریف فیلد (schema) ساخته می‌شود.
بیشتر ماژول‌های ساده (پرسنل، دوره‌ها، انبار PPE، معاینات و ...) از این
کامپوننت مشترک استفاده می‌کنند تا کد تکراری در برنامه کاهش یابد.

هر فیلد Audit (created_at/updated_at) به صورت خودکار توسط core.database
مدیریت می‌شود و هرگز در فرم به کاربر نمایش داده نمی‌شود.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QFormLayout,
    QMessageBox, QHeaderView, QSpinBox, QFileDialog
)
from PySide6.QtCore import Qt

from core.config import COLORS
from core.database import db
from ui.widgets.shamsi_date_picker import ShamsiDateEdit


class CrudPage(QWidget):
    """
    field ساختار:
      {"key": "first_name", "label": "نام", "type": "text"}
      {"key": "contract_type", "label": "نوع قرارداد", "type": "combo", "options": [...]}
      {"key": "hire_date_shamsi", "label": "تاریخ استخدام", "type": "date"}
      {"key": "description", "label": "شرح", "type": "textarea"}
      {"key": "stock_qty", "label": "موجودی", "type": "number"}
      {"key": "photo_path", "label": "تصویر پیوست", "type": "file"}
      {"key": "personnel_id", "label": "پرسنل", "type": "personnel_lookup"}
    """

    def __init__(self, table: str, title: str, fields: list, list_columns: list = None, parent=None):
        super().__init__(parent)
        self.table = table
        self.title = title
        self.fields = fields
        self.list_columns = list_columns or [f["key"] for f in fields]
        self.selected_id = None
        self.inputs = {}
        self._build_ui()
        self.reload()

    # ------------------------------------------------------------------
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        header = QLabel(self.title)
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        root.addWidget(header)

        body = QHBoxLayout()
        body.setSpacing(18)
        root.addLayout(body, 1)

        # ---------------- جدول ----------------
        table_box = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.list_columns))
        headers = [self._label_for(k) for k in self.list_columns]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.itemSelectionChanged.connect(self._on_select_row)
        self.table_widget.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                gridline-color: {COLORS['border']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_panel']};
                color: {COLORS['accent']};
                padding: 6px;
                border: none;
                font-weight: bold;
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['accent']};
                color: #1B2129;
            }}
        """)
        table_box.addWidget(self.table_widget)
        body.addLayout(table_box, 3)

        # ---------------- فرم ----------------
        form_container = QWidget()
        form_container.setStyleSheet(f"""
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        """)
        form_outer = QVBoxLayout(form_container)
        form_outer.setContentsMargins(16, 16, 16, 16)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        form_outer.addLayout(self.form_layout)

        for f in self.fields:
            widget = self._make_input(f)
            self.inputs[f["key"]] = widget
            self.form_layout.addRow(self._form_label(f["label"]), widget)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("ثبت")
        self.update_btn = QPushButton("ویرایش رکورد انتخاب‌شده")
        self.delete_btn = QPushButton("حذف رکورد انتخاب‌شده")
        self.clear_btn = QPushButton("فرم جدید")

        self.save_btn.clicked.connect(self._on_save)
        self.update_btn.clicked.connect(self._on_update)
        self.delete_btn.clicked.connect(self._on_delete)
        self.clear_btn.clicked.connect(self._clear_form)

        self.save_btn.setStyleSheet(self._btn_style(COLORS["accent"]))
        self.update_btn.setStyleSheet(self._btn_style(COLORS["safety_blue"]))
        self.delete_btn.setStyleSheet(self._btn_style(COLORS["safety_red"]))
        self.clear_btn.setStyleSheet(self._btn_style(COLORS["bg_input"], text=COLORS["text_primary"]))

        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.update_btn)
        btn_row.addWidget(self.delete_btn)
        btn_row.addWidget(self.clear_btn)
        form_outer.addLayout(btn_row)
        form_outer.addStretch(1)

        body.addWidget(form_container, 2)

    def _form_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color: {COLORS['text_secondary']};")
        return lbl

    def _btn_style(self, bg, text="#1B2129"):
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {text};
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ opacity: 0.9; }}
        """

    def _label_for(self, key):
        for f in self.fields:
            if f["key"] == key:
                return f["label"]
        return key

    # ------------------------------------------------------------------
    def _make_input(self, f):
        t = f["type"]
        if t == "text":
            w = QLineEdit()
            w.setStyleSheet(self._input_style())
            return w
        if t == "number":
            w = QSpinBox()
            w.setMaximum(1_000_000)
            w.setStyleSheet(self._input_style())
            return w
        if t == "textarea":
            w = QTextEdit()
            w.setFixedHeight(70)
            w.setStyleSheet(self._input_style())
            return w
        if t == "combo":
            w = QComboBox()
            w.addItems(f.get("options", []))
            w.setStyleSheet(self._input_style())
            return w
        if t == "date":
            return ShamsiDateEdit()
        if t == "file":
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            edit = QLineEdit()
            edit.setStyleSheet(self._input_style())
            btn = QPushButton("انتخاب فایل")
            btn.setStyleSheet(self._btn_style(COLORS["bg_input"], text=COLORS["text_primary"]))
            btn.clicked.connect(lambda: self._pick_file(edit))
            layout.addWidget(edit, 1)
            layout.addWidget(btn)
            container.line_edit = edit
            return container
        if t == "personnel_lookup":
            w = QComboBox()
            w.setStyleSheet(self._input_style())
            self._fill_personnel_combo(w)
            return w
        w = QLineEdit()
        w.setStyleSheet(self._input_style())
        return w

    def _input_style(self):
        return f"""
            QLineEdit, QTextEdit, QComboBox, QSpinBox {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 6px 8px;
            }}
        """

    def _pick_file(self, line_edit):
        path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل")
        if path:
            line_edit.setText(path)

    def _fill_personnel_combo(self, combo: QComboBox):
        combo.clear()
        rows = db.fetch_all(
            "SELECT id, personnel_code, first_name, last_name FROM personnel WHERE is_active = 1 ORDER BY first_name"
        )
        for r in rows:
            combo.addItem(f"{r['first_name']} {r['last_name']} ({r['personnel_code']})", r["id"])

    # ------------------------------------------------------------------
    def _collect_form_data(self) -> dict:
        data = {}
        for f in self.fields:
            key = f["key"]
            w = self.inputs[key]
            t = f["type"]
            if t == "text":
                data[key] = w.text().strip()
            elif t == "number":
                data[key] = w.value()
            elif t == "textarea":
                data[key] = w.toPlainText().strip()
            elif t == "combo":
                data[key] = w.currentText()
            elif t == "date":
                data[key] = w.value()
            elif t == "file":
                data[key] = w.line_edit.text().strip()
            elif t == "personnel_lookup":
                data[key] = w.currentData()
        return data

    def _validate(self, data: dict) -> bool:
        for f in self.fields:
            if f.get("required") and not str(data.get(f["key"], "")).strip():
                QMessageBox.warning(self, "خطا", f"تکمیل فیلد «{f['label']}» الزامی است.")
                return False
        for f in self.fields:
            if f["type"] == "date":
                w = self.inputs[f["key"]]
                if w.value() and not w.is_valid():
                    QMessageBox.warning(self, "خطا", f"تاریخ «{f['label']}» معتبر نیست (فرمت: 1403/01/01).")
                    return False
        return True

    # ------------------------------------------------------------------
    def _on_save(self):
        data = self._collect_form_data()
        if not self._validate(data):
            return
        try:
            db.insert_row(self.table, data)
        except Exception as e:
            QMessageBox.critical(self, "خطا در ثبت", str(e))
            return
        QMessageBox.information(self, "موفق", "رکورد با موفقیت ثبت شد.")
        self._clear_form()
        self.reload()

    def _on_update(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "خطا", "ابتدا یک رکورد را از جدول انتخاب کنید.")
            return
        data = self._collect_form_data()
        if not self._validate(data):
            return
        try:
            db.update_row(self.table, self.selected_id, data)
        except Exception as e:
            QMessageBox.critical(self, "خطا در ویرایش", str(e))
            return
        QMessageBox.information(self, "موفق", "رکورد ویرایش شد.")
        self._clear_form()
        self.reload()

    def _on_delete(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "خطا", "ابتدا یک رکورد را از جدول انتخاب کنید.")
            return
        confirm = QMessageBox.question(self, "تایید حذف", "آیا از حذف این رکورد مطمئن هستید؟")
        if confirm == QMessageBox.Yes:
            db.delete_row(self.table, self.selected_id)
            self._clear_form()
            self.reload()

    def _clear_form(self):
        self.selected_id = None
        for f in self.fields:
            w = self.inputs[f["key"]]
            t = f["type"]
            if t == "text":
                w.clear()
            elif t == "number":
                w.setValue(0)
            elif t == "textarea":
                w.clear()
            elif t == "combo":
                w.setCurrentIndex(0)
            elif t == "date":
                w.line_edit.clear()
            elif t == "file":
                w.line_edit.clear()
            elif t == "personnel_lookup":
                self._fill_personnel_combo(w)
        self.table_widget.clearSelection()

    def _on_select_row(self):
        row = self.table_widget.currentRow()
        if row < 0:
            return
        row_id = self.table_widget.item(row, 0).data(Qt.UserRole)
        self.selected_id = row_id
        record = db.fetch_one(f"SELECT * FROM {self.table} WHERE id = ?", (row_id,))
        if not record:
            return
        for f in self.fields:
            key = f["key"]
            w = self.inputs[key]
            value = record[key] if key in record.keys() else ""
            t = f["type"]
            if t == "text":
                w.setText(str(value or ""))
            elif t == "number":
                w.setValue(int(value or 0))
            elif t == "textarea":
                w.setPlainText(str(value or ""))
            elif t == "combo":
                idx = w.findText(str(value or ""))
                w.setCurrentIndex(idx if idx >= 0 else 0)
            elif t == "date":
                w.set_value(str(value or ""))
            elif t == "file":
                w.line_edit.setText(str(value or ""))
            elif t == "personnel_lookup":
                idx = w.findData(value)
                w.setCurrentIndex(idx if idx >= 0 else 0)

    # ------------------------------------------------------------------
    def reload(self):
        rows = db.fetch_all(f"SELECT * FROM {self.table} ORDER BY id DESC")
        self.table_widget.setRowCount(len(rows))
        for r_idx, row in enumerate(rows):
            for c_idx, key in enumerate(self.list_columns):
                value = row[key] if key in row.keys() else ""
                item = QTableWidgetItem(str(value if value is not None else ""))
                if c_idx == 0:
                    item.setData(Qt.UserRole, row["id"])
                self.table_widget.setItem(r_idx, c_idx, item)
