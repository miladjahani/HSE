"""
core/config.py
تنظیمات مرکزی برنامه: مسیرها، رنگ‌های تم صنعتی و ثابت‌های کلی
"""
import os
import sys


def get_base_dir() -> str:
    """
    مسیر پایه برنامه را برمی‌گرداند.
    وقتی برنامه به EXE تبدیل شود (PyInstaller)، فایل‌ها باید کنار EXE ذخیره شوند
    نه داخل پوشه موقت onefile، بنابراین از sys.executable استفاده می‌کنیم.
    """
    if getattr(sys, "frozen", False):
        # حالت اجرا به صورت EXE (PyInstaller)
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = get_base_dir()
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
DB_PATH = os.path.join(DATA_DIR, "hse_mine.db")

for _d in (DATA_DIR, BACKUP_DIR, EXPORT_DIR, ASSETS_DIR):
    os.makedirs(_d, exist_ok=True)

APP_NAME = "سامانه یکپارچه مدیریت HSE معدن"
APP_VERSION = "1.0.0"


# ---------------- پالت رنگی ----------------
DARK_COLORS = {
    "bg_main": "#12161C",
    "bg_panel": "#1B2129",
    "bg_card": "#212833",
    "bg_input": "#232B36",
    "border": "#2E3844",
    "sidebar": "#0E1116",
    "text_primary": "#E8ECF1",
    "text_secondary": "#8B96A5",
    "accent": "#F5A623",
    "accent_hover": "#FFB94D",
    "safety_green": "#2ECC71",
    "safety_yellow": "#F1C40F",
    "safety_orange": "#E67E22",
    "safety_red": "#E74C3C",
    "safety_blue": "#3498DB",
}

LIGHT_COLORS = {
    "bg_main": "#F5F7FA",
    "bg_panel": "#E4E7EB",
    "bg_card": "#FFFFFF",
    "bg_input": "#FFFFFF",
    "border": "#D1D5DB",
    "sidebar": "#1B2129", # Keep sidebar dark for industrial look
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "accent": "#F5A623",
    "accent_hover": "#E09612",
    "safety_green": "#27AE60",
    "safety_yellow": "#F39C12",
    "safety_orange": "#D35400",
    "safety_red": "#C0392B",
    "safety_blue": "#2980B9",
}

COLORS = DARK_COLORS.copy()

def set_theme(theme_name: str):
    global COLORS
    if theme_name == "light":
        COLORS.update(LIGHT_COLORS)
    else:
        COLORS.update(DARK_COLORS)


FONT_FAMILY = "Vazirmatn"  # فونت فارسی پیشنهادی؛ در صورت نبود، به فونت سیستم بازمی‌گردد
FONT_SIZE_BASE = 11

# نام ماه‌های شمسی برای Date Picker
JALALI_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
]
WEEKDAYS_FA = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
