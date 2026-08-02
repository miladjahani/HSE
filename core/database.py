"""
core/database.py
لایه دسترسی به دیتابیس SQLite.
- تمام جداول رویدادی دارای فیلدهای Audit خودکار هستند: created_at / updated_at
  که فقط توسط توابع این ماژول (نه کاربر) پر می‌شوند.
- دیتابیس به صورت فایل لوکال در DATA_DIR (کنار EXE یا AppData) نگهداری می‌شود.
"""
import sqlite3
import shutil
import os
from contextlib import contextmanager

from core.config import DB_PATH, BACKUP_DIR
from core.date_utils import now_shamsi_datetime_str


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_schema()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # ساخت اسکیمای دیتابیس
    # ------------------------------------------------------------------
    def _init_schema(self):
        with self.connect() as conn:
            c = conn.cursor()

            # تنظیمات فضای کاری (نام معدن/شرکت، لوگو، تنظیمات اولیه)
            c.execute("""
            CREATE TABLE IF NOT EXISTS workspace_settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                company_name TEXT NOT NULL,
                mine_name TEXT,
                logo_path TEXT,
                license_no TEXT,
                setup_completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # پرسنل
            c.execute("""
            CREATE TABLE IF NOT EXISTS personnel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personnel_code TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                national_id TEXT,
                position TEXT,
                department TEXT,
                contract_type TEXT,       -- رسمی/قراردادی/پیمانکار...
                contract_status TEXT,     -- فعال/پایان‌یافته/تعلیق
                hire_date_shamsi TEXT,
                phone TEXT,
                ppe_size TEXT,
                photo_path TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # Add ppe_size column if not exists
            try:
                c.execute("ALTER TABLE personnel ADD COLUMN ppe_size TEXT;")
            except sqlite3.OperationalError:
                pass

            # حوادث و شبه‌حوادث
            c.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_date_shamsi TEXT NOT NULL,
                incident_time TEXT,
                location TEXT,
                incident_type TEXT,        -- حادثه/شبه‌حادثه/نزدیک به حادثه
                severity TEXT,              -- جزئی/متوسط/شدید/فوت
                personnel_id INTEGER,
                description TEXT,
                root_cause TEXT,
                corrective_action TEXT,
                action_status TEXT DEFAULT 'باز',   -- باز/در حال انجام/بسته
                attachment_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE SET NULL
            );
            """)

            # انبار PPE
            c.execute("""
            CREATE TABLE IF NOT EXISTS ppe_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                item_code TEXT UNIQUE,
                unit TEXT DEFAULT 'عدد',
                stock_qty INTEGER NOT NULL DEFAULT 0,
                min_qty INTEGER NOT NULL DEFAULT 0,
                shelf_life_months INTEGER,   -- برای هشدار انقضا
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # تحویل PPE به پرسنل
            c.execute("""
            CREATE TABLE IF NOT EXISTS ppe_issuance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personnel_id INTEGER NOT NULL,
                ppe_item_id INTEGER NOT NULL,
                qty INTEGER NOT NULL DEFAULT 1,
                issue_date_shamsi TEXT NOT NULL,
                expiry_date_shamsi TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE,
                FOREIGN KEY (ppe_item_id) REFERENCES ppe_items(id) ON DELETE RESTRICT
            );
            """)

            # دوره‌های آموزشی
            c.execute("""
            CREATE TABLE IF NOT EXISTS training_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_title TEXT NOT NULL,
                validity_months INTEGER,   -- اعتبار دوره جهت هشدار سررسید تمدید
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # ثبت شرکت پرسنل در دوره‌ها
            c.execute("""
            CREATE TABLE IF NOT EXISTS training_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personnel_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                completion_date_shamsi TEXT NOT NULL,
                expiry_date_shamsi TEXT,
                score TEXT,
                certificate_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES training_courses(id) ON DELETE RESTRICT
            );
            """)

            # معاینات طب کار (ادیومتری/اسپیرومتری/عمومی)
            c.execute("""
            CREATE TABLE IF NOT EXISTS medical_exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personnel_id INTEGER NOT NULL,
                exam_type TEXT NOT NULL,      -- ادیومتری/اسپیرومتری/عمومی/...
                exam_date_shamsi TEXT NOT NULL,
                next_due_date_shamsi TEXT,
                result TEXT,                  -- سالم/نیازمند پیگیری/...
                notes TEXT,
                attachment_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
            );
            """)

            # تشویق و تنبیه
            c.execute("""
            CREATE TABLE IF NOT EXISTS disciplinary_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personnel_id INTEGER NOT NULL,
                record_type TEXT NOT NULL,     -- تشویق / تنبیه
                title TEXT,
                description TEXT,
                event_date_shamsi TEXT NOT NULL,
                reward_or_penalty TEXT,         -- نوع پاداش یا جریمه
                registered_by TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
            );
            """)

            for idx_sql in [
                "CREATE INDEX IF NOT EXISTS idx_personnel_code ON personnel(personnel_code);",
                "CREATE INDEX IF NOT EXISTS idx_incidents_date ON incidents(incident_date_shamsi);",
                "CREATE INDEX IF NOT EXISTS idx_ppe_issuance_personnel ON ppe_issuance(personnel_id);",
                "CREATE INDEX IF NOT EXISTS idx_training_personnel ON training_records(personnel_id);",
                "CREATE INDEX IF NOT EXISTS idx_medical_personnel ON medical_exams(personnel_id);",
                "CREATE INDEX IF NOT EXISTS idx_disciplinary_personnel ON disciplinary_records(personnel_id);",
            ]:
                c.execute(idx_sql)

    # ------------------------------------------------------------------
    # فضای کاری
    # ------------------------------------------------------------------
    def is_setup_completed(self) -> bool:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT setup_completed FROM workspace_settings WHERE id = 1"
            ).fetchone()
            return bool(row and row["setup_completed"])

    def save_workspace_setup(self, company_name, mine_name, logo_path, license_no=""):
        ts = now_shamsi_datetime_str()
        with self.connect() as conn:
            conn.execute("""
                INSERT INTO workspace_settings (id, company_name, mine_name, logo_path, license_no,
                    setup_completed, created_at, updated_at)
                VALUES (1, ?, ?, ?, ?, 1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    company_name=excluded.company_name,
                    mine_name=excluded.mine_name,
                    logo_path=excluded.logo_path,
                    license_no=excluded.license_no,
                    setup_completed=1,
                    updated_at=excluded.updated_at;
            """, (company_name, mine_name, logo_path, license_no, ts, ts))

    def get_workspace(self):
        with self.connect() as conn:
            return conn.execute("SELECT * FROM workspace_settings WHERE id = 1").fetchone()

    # ------------------------------------------------------------------
    # کمکی: درج/ویرایش عمومی با پر کردن خودکار Audit Fields
    # ------------------------------------------------------------------
    def insert_row(self, table: str, data: dict) -> int:
        ts = now_shamsi_datetime_str()
        data = dict(data)
        data["created_at"] = ts
        data["updated_at"] = ts
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        with self.connect() as conn:
            cur = conn.execute(
                f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
                list(data.values()),
            )
            return cur.lastrowid

    def update_row(self, table: str, row_id: int, data: dict):
        data = dict(data)
        data["updated_at"] = now_shamsi_datetime_str()
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        with self.connect() as conn:
            conn.execute(
                f"UPDATE {table} SET {set_clause} WHERE id = ?",
                list(data.values()) + [row_id],
            )

    def delete_row(self, table: str, row_id: int):
        with self.connect() as conn:
            conn.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))

    def fetch_all(self, query: str, params: tuple = ()):
        with self.connect() as conn:
            return conn.execute(query, params).fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        with self.connect() as conn:
            return conn.execute(query, params).fetchone()

    # ------------------------------------------------------------------
    # پشتیبان‌گیری / بازیابی
    # ------------------------------------------------------------------
    def backup_database(self) -> str:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        stamp = now_shamsi_datetime_str().replace("/", "-").replace(":", "-").replace(" ", "_")
        dest = os.path.join(BACKUP_DIR, f"hse_backup_{stamp}.db")
        shutil.copy2(self.db_path, dest)
        return dest

    def restore_database(self, backup_file_path: str):
        shutil.copy2(backup_file_path, self.db_path)


# نمونه Singleton برای استفاده در کل برنامه
db = Database()
