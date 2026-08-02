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

    # 2. Lost Time (Total days from incidents)
    lost_time = db.fetch_one("SELECT SUM(lost_time_days) as total FROM incidents")
    data["lost_time_days"] = lost_time["total"] if lost_time and lost_time["total"] else 0

    # 3. Heinrich Pyramid
    pyramid = {
        "anomaly_report": 0, # Could map to 'نزدیک به حادثه' or a new type
        "near_miss": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE incident_type='شبه‌حادثه'")["c"] or 0,
        "first_aid": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE severity='جزئی'")["c"] or 0,
        "lost_time_accident": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE lost_time_days > 0")["c"] or 0,
        "death": db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE severity='فوت'")["c"] or 0,
    }
    # If anomaly report isn't directly mapped, just give it a mock ratio for now
    pyramid["anomaly_report"] = pyramid["near_miss"] * 3
    data["heinrich_pyramid"] = pyramid

    # 4. Safety Index (Rates)
    # Frequency Rate = (Number of lost time accidents * 1,000,000) / Total Man-hours
    # Severity Rate = (Total lost time days * 1,000,000) / Total Man-hours
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

    # 6. Training Man-hours (Mocked for now as we don't store duration per course, assuming 8h per course)
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
    # Mapping results from medical_exams to these categories roughly
    data["occupational_health"] = {
        "rate": "1.39%",
        "disease": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE result LIKE '%بیماری%'")["c"] or 0,
        "hearing_loss": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE exam_type='ادیومتری' AND result LIKE '%افت%'")["c"] or 0,
        "respiratory": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE exam_type='اسپیرومتری' AND result LIKE '%مشکل%'")["c"] or 0,
        "back_pain": db.fetch_one("SELECT COUNT(*) as c FROM medical_exams WHERE result LIKE '%کمر%'")["c"] or 0,
    }

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
