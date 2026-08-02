"""
ui/backup.py
پشتیبان‌گیری و بازیابی دیتابیس لوکال.
"""
import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QMessageBox, QFileDialog
)

from core.config import COLORS, BACKUP_DIR
from core.database import db


class BackupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.reload()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        header = QLabel("پشتیبان‌گیری و بازیابی دیتابیس")
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        root.addWidget(header)

        warn = QLabel(
            "پیشنهاد می‌شود به‌طور منظم (مثلاً هفتگی) از دیتابیس نسخه پشتیبان تهیه کنید. "
            "بازیابی، دیتابیس فعلی را با نسخه انتخابی جایگزین می‌کند."
        )
        warn.setWordWrap(True)
        warn.setStyleSheet(f"color: {COLORS['text_secondary']};")
        root.addWidget(warn)

        btn_row = QHBoxLayout()
        backup_btn = QPushButton("تهیه نسخه پشتیبان اکنون")
        restore_btn = QPushButton("بازیابی از فایل پشتیبان دیگر")
        backup_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']}; color: #1B2129;
                border: none; border-radius: 6px; padding: 10px 16px; font-weight: bold;
            }}
        """)
        restore_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['safety_red']}; color: #1B2129;
                border: none; border-radius: 6px; padding: 10px 16px; font-weight: bold;
            }}
        """)
        backup_btn.clicked.connect(self._do_backup)
        restore_btn.clicked.connect(self._do_restore_from_file)
        btn_row.addWidget(backup_btn)
        btn_row.addWidget(restore_btn)
        root.addLayout(btn_row)

        list_label = QLabel("نسخه‌های پشتیبان موجود:")
        list_label.setStyleSheet(f"color: {COLORS['text_primary']}; margin-top: 10px;")
        root.addWidget(list_label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        root.addWidget(self.list_widget, 1)

        restore_selected_btn = QPushButton("بازیابی نسخه انتخاب‌شده از لیست")
        restore_selected_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 6px; padding: 8px;
            }}
        """)
        restore_selected_btn.clicked.connect(self._do_restore_from_list)
        root.addWidget(restore_selected_btn)

    def reload(self):
        self.list_widget.clear()
        if not os.path.isdir(BACKUP_DIR):
            return
        files = sorted(os.listdir(BACKUP_DIR), reverse=True)
        for f in files:
            if f.endswith(".db"):
                self.list_widget.addItem(f)

    def _do_backup(self):
        path = db.backup_database()
        QMessageBox.information(self, "موفق", f"نسخه پشتیبان با موفقیت ایجاد شد:\n{path}")
        self.reload()

    def _do_restore_from_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "انتخاب فایل پشتیبان", BACKUP_DIR, "Database (*.db)")
        if not path:
            return
        self._confirm_and_restore(path)

    def _do_restore_from_list(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "خطا", "یک نسخه پشتیبان را از لیست انتخاب کنید.")
            return
        path = os.path.join(BACKUP_DIR, item.text())
        self._confirm_and_restore(path)

    def _confirm_and_restore(self, path):
        confirm = QMessageBox.question(
            self, "تایید بازیابی",
            "با این کار تمام داده‌های فعلی با نسخه پشتیبان جایگزین می‌شود. ادامه می‌دهید؟"
        )
        if confirm == QMessageBox.Yes:
            db.restore_database(path)
            QMessageBox.information(
                self, "موفق",
                "بازیابی انجام شد. لطفاً برنامه را ببندید و دوباره اجرا کنید تا تغییرات اعمال شود."
            )
