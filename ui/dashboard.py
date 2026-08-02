"""
ui/dashboard.py
داشبورد اصلی: کارت‌های KPI (آمار حوادث باز، پرسنل فاقد PPE، سررسید طب کار،
آمار تشویق/تنبیه) به‌همراه نمودار میله‌ای حوادث در ۶ ماه اخیر.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame
from PySide6.QtCore import Qt

from core.config import COLORS
from core.database import db
from core.date_utils import days_between

try:
    from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
    HAS_CHARTS = True
except Exception:
    HAS_CHARTS = False


class KpiCard(QFrame):
    def __init__(self, title, value, color, subtitle=""):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-right: 4px solid {color};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)

        val_lbl = QLabel(str(value))
        val_lbl.setStyleSheet(f"color: {color}; font-size: 26px; font-weight: bold;")
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        title_lbl.setWordWrap(True)

        layout.addWidget(val_lbl)
        layout.addWidget(title_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
            layout.addWidget(sub_lbl)


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        header = QLabel("داشبورد مدیریت HSE")
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 18px; font-weight: bold;")
        root.addWidget(header)

        self.cards_grid = QGridLayout()
        self.cards_grid.setSpacing(14)
        root.addLayout(self.cards_grid)

        self.chart_container = QVBoxLayout()
        root.addLayout(self.chart_container, 1)

        self.reload()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def reload(self):
        self._clear_layout(self.cards_grid)
        self._clear_layout(self.chart_container)

        open_incidents = db.fetch_one(
            "SELECT COUNT(*) c FROM incidents WHERE action_status != 'بسته'"
        )["c"]

        active_personnel = db.fetch_one(
            "SELECT COUNT(*) c FROM personnel WHERE is_active = 1"
        )["c"]

        issued_personnel_ids = {
            r["personnel_id"] for r in db.fetch_all("SELECT DISTINCT personnel_id FROM ppe_issuance")
        }
        missing_ppe = max(active_personnel - len(issued_personnel_ids), 0)

        medical_due_soon = 0
        for r in db.fetch_all("SELECT next_due_date_shamsi FROM medical_exams WHERE next_due_date_shamsi IS NOT NULL"):
            try:
                if 0 <= days_between(r["next_due_date_shamsi"]) <= 30:
                    medical_due_soon += 1
            except Exception:
                pass

        rewards = db.fetch_one(
            "SELECT COUNT(*) c FROM disciplinary_records WHERE record_type = 'تشویق'"
        )["c"]
        penalties = db.fetch_one(
            "SELECT COUNT(*) c FROM disciplinary_records WHERE record_type = 'تنبیه'"
        )["c"]

        cards = [
            ("پرسنل فعال", active_personnel, COLORS["safety_blue"], ""),
            ("حوادث باز", open_incidents, COLORS["safety_red"], "نیازمند اقدام اصلاحی"),
            ("پرسنل فاقد PPE", missing_ppe, COLORS["safety_orange"], "بدون سابقه تحویل"),
            ("سررسید طب کار (۳۰ روز آینده)", medical_due_soon, COLORS["safety_yellow"], ""),
            ("تشویق ثبت‌شده", rewards, COLORS["safety_green"], ""),
            ("تنبیه ثبت‌شده", penalties, COLORS["safety_red"], ""),
        ]
        for i, (title, value, color, sub) in enumerate(cards):
            self.cards_grid.addWidget(KpiCard(title, value, color, sub), i // 3, i % 3)

        self._render_incident_chart()

    def _render_incident_chart(self):
        title = QLabel("روند حوادث و شبه‌حوادث (۶ ماه اخیر)")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 14px; font-weight: bold;")
        self.chart_container.addWidget(title)

        rows = db.fetch_all(
            "SELECT substr(incident_date_shamsi, 1, 7) ym, COUNT(*) c FROM incidents "
            "GROUP BY ym ORDER BY ym DESC LIMIT 6"
        )
        rows = list(reversed(rows))

        if not HAS_CHARTS or not rows:
            placeholder = QLabel("داده کافی برای رسم نمودار وجود ندارد." if not rows else
                                  "ماژول نمودار (QtCharts) در دسترس نیست.")
            placeholder.setStyleSheet(f"color: {COLORS['text_secondary']};")
            self.chart_container.addWidget(placeholder)
            return

        bar_set = QBarSet("تعداد حوادث")
        bar_set.setColor(Qt.GlobalColor.transparent)
        categories = []
        for r in rows:
            bar_set.append(r["c"])
            categories.append(r["ym"])

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        chart.legend().hide()

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setStyleSheet(f"background-color: {COLORS['bg_card']}; border-radius: 8px;")
        chart_view.setMinimumHeight(240)
        self.chart_container.addWidget(chart_view)
