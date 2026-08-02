# سامانه یکپارچه مدیریت HSE معدن (نسخه ۲.۰.۰)

نرم‌افزار دسکتاپ کاملاً آفلاین برای مدیریت HSE معادن.
این نسخه به معماری مدرن **React (Vite) + FastAPI + PyWebView** ارتقا یافته است و همچنان از پایگاه داده لوکال **SQLite** استفاده می‌کند.

## تغییرات نسخه جدید
- بازنویسی کامل رابط کاربری به React جهت داشتن ظاهر مدرن، واکنش‌گرا و انیمیشن‌های جذاب.
- اضافه شدن داشبورد جامع و حرفه‌ای شامل هرم هاینریش، شاخص‌های ایمنی (ضریب شدت/تکرار)، شاخص‌های بهداشت حرفه‌ای و شاخص‌های محیط زیستی (مصرف آب، برق، گاز).
- مهاجرت از PySide6 به FastAPI (به عنوان وب‌سرور داخلی) و PyWebView (برای نمایش پنجره دسکتاپ).

## پیش‌نیازها
- Node.js 18+ (فقط برای توسعه و بیلد فرانت‌اند)

## اجرای پروژه در محیط توسعه

ابتدا فرانت‌اند (React) را بیلد کنید:
cd ui_react
npm install
npm run build


سپس بک‌اند را در پایتون اجرا کنید:
cd ..
virtualenv venv
venv\Scripts\activate

pip install -r requirements-fastapi.txt
python main.py

## ساخت فایل نصب/اجرایی (EXE) در ویندوز

مرحله ۱: ابتدا مطمئن شوید آخرین تغییرات React را بیلد کرده‌اید:
cd ui_react
npm run build
cd ..

مرحله ۲: با استفاده از PyInstaller فایل نهایی را بسازید:
pyinstaller --noconfirm --onefile --windowed --name "HSE_Mine_Manager_V2" --icon "assets\app_icon.ico" --add-data "ui_react\dist;ui_react\dist" --add-data "assets;assets" main.py

فایل EXE نهایی در پوشه `dist` قرار می‌گیرد. با اولین اجرای آن روی هر سیستمی، دیتابیس لوکال ساخته می‌شود و نرم‌افزار به صورت آفلاین کار می‌کند.
