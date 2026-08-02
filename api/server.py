from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Add parent dir to path to import core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import db
from core.date_utils import now_shamsi_datetime_str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers
def row_to_dict(row):
    return dict(row) if row else None

def rows_to_list(rows):
    return [dict(r) for r in rows] if rows else []


# CRUD Endpoints builder
def create_crud_endpoints(table_name):
    @app.get(f"/api/{table_name}")
    def get_all():
        return rows_to_list(db.fetch_all(f"SELECT * FROM {table_name} ORDER BY id DESC"))

    @app.get(f"/api/{table_name}/{{item_id}}")
    def get_one(item_id: int):
        row = db.fetch_one(f"SELECT * FROM {table_name} WHERE id = ?", (item_id,))
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        return row_to_dict(row)

    @app.post(f"/api/{table_name}")
    async def create_item(request: Request):
        data = await request.json()
        try:
            item_id = db.insert_row(table_name, data)
            return {"id": item_id, "message": "Created successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.put(f"/api/{table_name}/{{item_id}}")
    async def update_item(item_id: int, request: Request):
        data = await request.json()
        try:
            db.update_row(table_name, item_id, data)
            return {"id": item_id, "message": "Updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.delete(f"/api/{table_name}/{{item_id}}")
    def delete_item(item_id: int):
        try:
            db.delete_row(table_name, item_id)
            return {"message": "Deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# Register CRUD for all tables
TABLES = [
    "personnel", "incidents", "ppe_items", "ppe_issuance",
    "training_courses", "training_records", "medical_exams",
    "disciplinary_records", "man_hours", "work_permits", "environmental_metrics"
]
for table in TABLES:
    create_crud_endpoints(table)


# Dashboard Endpoint

@app.get("/api/personnel/{personnel_id}/profile")
def get_personnel_profile(personnel_id: int):
    # Fetch all data related to a single personnel
    personnel = db.fetch_one("SELECT * FROM personnel WHERE id = ?", (personnel_id,))
    if not personnel:
        raise HTTPException(status_code=404, detail="Personnel not found")

    data = row_to_dict(personnel)

    # Incidents
    data["incidents"] = rows_to_list(db.fetch_all("SELECT * FROM incidents WHERE personnel_id = ? ORDER BY incident_date_shamsi DESC", (personnel_id,)))

    # Medical Exams
    data["medical_exams"] = rows_to_list(db.fetch_all("SELECT * FROM medical_exams WHERE personnel_id = ? ORDER BY exam_date_shamsi DESC", (personnel_id,)))

    # Training Records
    data["training_records"] = rows_to_list(db.fetch_all('''
        SELECT tr.*, tc.course_title
        FROM training_records tr
        JOIN training_courses tc ON tr.course_id = tc.id
        WHERE tr.personnel_id = ?
        ORDER BY tr.completion_date_shamsi DESC
    ''', (personnel_id,)))

    # PPE Issuance
    data["ppe_issuance"] = rows_to_list(db.fetch_all('''
        SELECT pi.*, p.item_name
        FROM ppe_issuance pi
        JOIN ppe_items p ON pi.ppe_item_id = p.id
        WHERE pi.personnel_id = ?
        ORDER BY pi.issue_date_shamsi DESC
    ''', (personnel_id,)))

    # Disciplinary Records
    data["disciplinary_records"] = rows_to_list(db.fetch_all("SELECT * FROM disciplinary_records WHERE personnel_id = ? ORDER BY event_date_shamsi DESC", (personnel_id,)))

    return data

@app.get("/api/reports/export")
def generate_reports(tables: str, start_date: str = None, end_date: str = None, personnel_ids: str = None):
    try:
        import pandas as pd
    except ImportError:
        raise HTTPException(status_code=500, detail="Pandas library not installed. Please pip install pandas openpyxl")

    table_list = tables.split(",")
    p_ids = personnel_ids.split(",") if personnel_ids else []

    TABLE_META = {
        "personnel": {"date_col": "hire_date_shamsi", "personnel_col": "id"},
        "incidents": {"date_col": "incident_date_shamsi", "personnel_col": "personnel_id"},
        "ppe_items": {"date_col": "created_at", "personnel_col": None},
        "ppe_issuance": {"date_col": "issue_date_shamsi", "personnel_col": "personnel_id"},
        "training_courses": {"date_col": "created_at", "personnel_col": None},
        "training_records": {"date_col": "completion_date_shamsi", "personnel_col": "personnel_id"},
        "medical_exams": {"date_col": "exam_date_shamsi", "personnel_col": "personnel_id"},
        "disciplinary_records": {"date_col": "event_date_shamsi", "personnel_col": "personnel_id"},
        "man_hours": {"date_col": "month_shamsi", "personnel_col": None},
        "work_permits": {"date_col": "month_shamsi", "personnel_col": None},
        "environmental_metrics": {"date_col": "month_shamsi", "personnel_col": None},
    }

    from core.config import EXPORT_DIR
    import os
    from datetime import datetime

    filename = f"HSE_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(EXPORT_DIR, filename)

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        for t in table_list:
            query = f"SELECT * FROM {t}"
            params = []
            conditions = []
            meta = TABLE_META.get(t)

            if meta:
                if start_date:
                    conditions.append(f"{meta['date_col']} >= ?")
                    params.append(start_date)
                if end_date:
                    conditions.append(f"{meta['date_col']} <= ?")
                    params.append(end_date)
                if meta['personnel_col'] and p_ids:
                    placeholders = ",".join(["?"] * len(p_ids))
                    conditions.append(f"{meta['personnel_col']} IN ({placeholders})")
                    params.extend(p_ids)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            rows = db.fetch_all(query, params)
            if not rows:
                df = pd.DataFrame([{"Message": "بدون داده"}])
            else:
                df = pd.DataFrame([dict(r) for r in rows])

            sheet_name = t[:31] # Excel sheet name limit
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return FileResponse(path=filepath, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.get("/api/dashboard")
def get_dashboard_data():
    data = {}

    # 1. Total Employees & Man Hours (from latest man_hours record)
    latest_mh = db.fetch_one("SELECT total_employees, man_hours FROM man_hours ORDER BY month_shamsi DESC LIMIT 1")
    if latest_mh:
        data["total_employees"] = latest_mh["total_employees"]
        data["man_hours"] = latest_mh["man_hours"]
    else:
        # Fallback to current personnel count if no mh record
        active = db.fetch_one("SELECT COUNT(*) as c FROM personnel WHERE is_active=1")
        data["total_employees"] = active["c"] if active else 0
        data["man_hours"] = 0

    # --- Old KPIs ---
    open_incidents = db.fetch_one("SELECT COUNT(*) c FROM incidents WHERE action_status != 'بسته'")["c"]
    data["open_incidents"] = open_incidents or 0

    active_personnel = data["total_employees"]
    issued_personnel_ids = {r["personnel_id"] for r in db.fetch_all("SELECT DISTINCT personnel_id FROM ppe_issuance")}
    data["missing_ppe"] = max(active_personnel - len(issued_personnel_ids), 0)

    medical_due_soon = 0
    from core.date_utils import days_between
    for r in db.fetch_all("SELECT next_due_date_shamsi FROM medical_exams WHERE next_due_date_shamsi IS NOT NULL"):
        try:
            if 0 <= days_between(r["next_due_date_shamsi"]) <= 30:
                medical_due_soon += 1
        except:
            pass
    data["medical_due_soon"] = medical_due_soon

    rewards = db.fetch_one("SELECT COUNT(*) c FROM disciplinary_records WHERE record_type = 'تشویق'")["c"]
    penalties = db.fetch_one("SELECT COUNT(*) c FROM disciplinary_records WHERE record_type = 'تنبیه'")["c"]
    data["rewards"] = rewards or 0
    data["penalties"] = penalties or 0
    # ----------------

    # 2. Lost Time (Total days from incidents)
    lost_time = db.fetch_one("SELECT SUM(lost_time_days) as total FROM incidents")
    data["lost_time_days"] = lost_time["total"] if lost_time and lost_time["total"] else 0

    # 3. Heinrich Pyramid
    pyramid = {
        "anomaly_report": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE incident_type='نزدیک به حادثه'")["c"] or 0,
        "near_miss": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE incident_type='شبه‌حادثه'")["c"] or 0,
        "first_aid": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE severity='جزئی'")["c"] or 0,
        "lost_time_accident": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE lost_time_days > 0")["c"] or 0,
        "death": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE severity='فوت'")["c"] or 0,
    }
    data["heinrich_pyramid"] = pyramid

    # 4. Safety Index (Rates)
    total_mh_all_time = db.fetch_one("SELECT SUM(man_hours) as total FROM man_hours")["total"] or 0
    if total_mh_all_time > 0:
        data["frequency_rate"] = round((pyramid["lost_time_accident"] * 1000000) / total_mh_all_time, 2)
        data["severity_rate"] = round((data["lost_time_days"] * 1000000) / total_mh_all_time, 3)
    else:
        data["frequency_rate"] = 0
        data["severity_rate"] = 0

    # 5. Work Permit
    permits = db.fetch_one("SELECT SUM(permit_count) as total FROM work_permits")
    data["work_permits"] = permits["total"] if permits and permits["total"] else 0

    # 6. Training Man-hours
    training_count = db.fetch_one("SELECT COUNT(*) as c FROM training_records")["c"] or 0
    data["training_man_hours"] = training_count * 8

    # 7. MBDA (Mean Time Between Accidents - mock value based on days since last accident)
    data["mbda"] = 0

    # 8. Comparison HSE Index (Mock data for previous year since we might not have it)
    data["comparison"] = {
        "safe_t_score": -1.93,
        "severity_rate_prev": 0.263,
        "severity_rate_curr": data["severity_rate"],
        "frequency_rate_prev": 8.03,
        "frequency_rate_curr": data["frequency_rate"]
    }

    # 9. Risk Assessment HSE
    data["risk_assessment"] = {
        "critical": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE risk_assessment_level='Critical'")["c"] or 0,
        "high": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE risk_assessment_level='High'")["c"] or 0,
        "medium": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE risk_assessment_level='Medium'")["c"] or 0,
        "low": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE risk_assessment_level='Low'")["c"] or 0,
    }

    # 10. Occupational Health Indicators
    data["occupational_health"] = {
        "disease": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE result LIKE '%بیماری%'")["c"] or 0,
        "hearing_loss": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE exam_type='ادیومتری' AND result LIKE '%افت%'")["c"] or 0,
        "respiratory": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE exam_type='اسپیرومتری' AND result LIKE '%مشکل%'")["c"] or 0,
        "back_pain": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE result LIKE '%کمر%'")["c"] or 0,
    }
    # Calculate rate based on total exams
    total_exams = db.fetch_one("SELECT COUNT(*) as c FROM medical_exams")["c"] or 1
    total_sick = data["occupational_health"]["disease"] + data["occupational_health"]["hearing_loss"] + data["occupational_health"]["respiratory"] + data["occupational_health"]["back_pain"]
    data["occupational_health"]["rate"] = str(round((total_sick / total_exams) * 100, 2)) + "%"

    # 11. Environmental Indicators
    env = db.fetch_one("SELECT SUM(water_consumption_m3) as w_c, SUM(water_recovery_m3) as w_r, SUM(energy_consumption_kwh) as e_c, SUM(gas_consumption_m2) as g_c FROM environmental_metrics")
    if env and env["w_c"] is not None:
        data["environmental"] = {
            "water_consumption": env["w_c"],
            "water_recovery": env["w_r"],
            "energy_consumption": env["e_c"],
            "gas_consumption": env["g_c"]
        }
    else:
        data["environmental"] = {
            "water_consumption": 0, "water_recovery": 0,
            "energy_consumption": 0, "gas_consumption": 0
        }

    return data


import os
from core.config import BACKUP_DIR

@app.get("/api/backup/list")
def list_backups():
    backups = []
    if os.path.exists(BACKUP_DIR):
        for f in os.listdir(BACKUP_DIR):
            if f.endswith(".db"):
                fpath = os.path.join(BACKUP_DIR, f)
                backups.append({
                    "name": f,
                    "path": fpath,
                    "size": os.path.getsize(fpath)
                })
    # Sort by name descending (latest first)
    backups.sort(key=lambda x: x["name"], reverse=True)
    return backups

@app.post("/api/backup")
def create_backup():
    try:
        path = db.backup_database()
        return {"message": "پشتیبان‌گیری با موفقیت انجام شد.", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/restore")
async def restore_backup(request: Request):
    data = await request.json()
    path = data.get("path")
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=400, detail="فایل پیدا نشد.")
    try:
        db.restore_database(path)
        return {"message": "بازیابی دیتابیس با موفقیت انجام شد. برنامه را مجدد اجرا کنید."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workspace")
def get_workspace():
    return row_to_dict(db.get_workspace())

@app.post("/api/workspace")
async def save_workspace(request: Request):
    data = await request.json()
    db.save_workspace_setup(
        company_name=data.get("company_name", ""),
        mine_name=data.get("mine_name", ""),
        logo_path=data.get("logo_path", ""),
        license_no=data.get("license_no", "")
    )
    return {"message": "Workspace saved"}

@app.put("/api/theme")
async def update_theme(request: Request):
    data = await request.json()
    db.update_theme(data.get("theme", "dark"))
    return {"message": "Theme updated"}


# Serve the React build
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui_react", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "React build not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
