"""
ui/setup_wizard.py
در اولین اجرای برنامه نمایش داده می‌شود: نام معدن/شرکت و لوگو گرفته می‌شود
و رکورد workspace_settings ساخته می‌شود.
"""
import shutil
import os

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from core.config import COLORS, ASSETS_DIR, APP_NAME
from core.database import db


class SetupWizard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("راه‌اندازی اولیه فضای کاری")
        self.setFixedSize(460, 420)
        self.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        self.logo_path = ""
        self._build_ui()

    def _input_style(self):
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        """

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        title = QLabel(f"به {APP_NAME} خوش آمدید")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['accent']}; font-size: 15px; font-weight: bold;")
        layout.addWidget(title)

        sub = QLabel("لطفاً اطلاعات اولیه فضای کاری خود را وارد کنید. این اطلاعات فقط یک بار ثبت می‌شود.")
        sub.setWordWrap(True)
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        layout.addWidget(sub)

        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("نام شرکت *")
        self.company_input.setStyleSheet(self._input_style())
        layout.addWidget(self.company_input)

        self.mine_input = QLineEdit()
        self.mine_input.setPlaceholderText("نام معدن")
        self.mine_input.setStyleSheet(self._input_style())
        layout.addWidget(self.mine_input)

        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("شماره مجوز / کد پروانه بهره‌برداری (اختیاری)")
        self.license_input.setStyleSheet(self._input_style())
        layout.addWidget(self.license_input)

        logo_row = QHBoxLayout()
        self.logo_preview = QLabel("بدون لوگو")
        self.logo_preview.setFixedSize(80, 80)
        self.logo_preview.setAlignment(Qt.AlignCenter)
        self.logo_preview.setStyleSheet(f"""
            border: 1px dashed {COLORS['border']};
            border-radius: 8px;
            color: {COLORS['text_secondary']};
        """)
        logo_btn = QPushButton("انتخاب لوگو")
        logo_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        logo_btn.clicked.connect(self._pick_logo)
        logo_row.addWidget(self.logo_preview)
        logo_row.addWidget(logo_btn, 1)
        layout.addLayout(logo_row)

        layout.addStretch(1)

        finish_btn = QPushButton("ایجاد فضای کاری و ورود به برنامه")
        finish_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: #1B2129;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent_hover']}; }}
        """)
        finish_btn.clicked.connect(self._finish)
        layout.addWidget(finish_btn)

    def _pick_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "انتخاب لوگو", filter="Images (*.png *.jpg *.jpeg)")
        if path:
            os.makedirs(ASSETS_DIR, exist_ok=True)
            ext = os.path.splitext(path)[1]
            dest = os.path.join(ASSETS_DIR, f"logo{ext}")
            shutil.copy2(path, dest)
            self.logo_path = dest
            pix = QPixmap(dest).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_preview.setPixmap(pix)
            self.logo_preview.setText("")

    def _finish(self):
        company = self.company_input.text().strip()
        if not company:
            QMessageBox.warning(self, "خطا", "وارد کردن نام شرکت الزامی است.")
            return
        db.save_workspace_setup(
            company_name=company,
            mine_name=self.mine_input.text().strip(),
            logo_path=self.logo_path,
            license_no=self.license_input.text().strip(),
        )
        self.accept()
