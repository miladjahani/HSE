"""
core/date_utils.py
تمام عملیات تاریخ/زمان شمسی برنامه از این ماژول عبور می‌کند تا
یکپارچگی فرمت تاریخ (برای ذخیره در دیتابیس و نمایش) تضمین شود.

فرمت ذخیره‌سازی در دیتابیس: 'YYYY/MM/DD HH:MM:SS' (رشته، قابل Sort صحیح
چون همیشه با صفر پرشده و طول ثابت است) -> مثال: 1403/05/12 14:30:05
"""
import jdatetime

DB_DATETIME_FMT = "%Y/%m/%d %H:%M:%S"
DB_DATE_FMT = "%Y/%m/%d"
DISPLAY_DATE_FMT = "%Y/%m/%d"


def now_shamsi_datetime_str() -> str:
    """تاریخ و ساعت لحظه‌ی حال به شمسی، برای فیلدهای Audit (Created_At/Updated_At)."""
    return jdatetime.datetime.now().strftime(DB_DATETIME_FMT)


def now_shamsi_date_str() -> str:
    return jdatetime.date.today().strftime(DB_DATE_FMT)


def gregorian_to_shamsi_str(g_date) -> str:
    """تبدیل تاریخ میلادی (datetime.date) به رشته شمسی برای نمایش در Date Picker."""
    j = jdatetime.date.fromgregorian(date=g_date)
    return j.strftime(DB_DATE_FMT)


def shamsi_str_to_gregorian(shamsi_str: str):
    """تبدیل رشته شمسی 'YYYY/MM/DD' به datetime.date میلادی (برای QDate در ویجت‌ها)."""
    y, m, d = [int(x) for x in shamsi_str.split("/")]
    return jdatetime.date(y, m, d).togregorian()


def is_valid_shamsi_date(shamsi_str: str) -> bool:
    try:
        y, m, d = [int(x) for x in shamsi_str.strip().split("/")]
        jdatetime.date(y, m, d)
        return True
    except Exception:
        return False


def shamsi_today_ymd():
    t = jdatetime.date.today()
    return t.year, t.month, t.day


def days_between(shamsi_date_str: str, from_today: bool = True) -> int:
    """تعداد روزهای فاصله‌ی یک تاریخ شمسی تا امروز (برای هشدار سررسید/انقضا)."""
    y, m, d = [int(x) for x in shamsi_date_str.split("/")]
    target = jdatetime.date(y, m, d)
    today = jdatetime.date.today()
    delta = (target.togregorian() - today.togregorian()).days
    return delta
