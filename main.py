import os
import sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Ensure root directory is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from src.database.db import init_db
from src.api.routes import api_router

# Initialize FastAPI App
app = FastAPI(
    title="S&P Global × CRISIL AI/NLP Financial Risk Engine",
    description="Enterprise Multi-Source AI Risk Engine with Tactical Index Rebalancer and Strategic Wholesale Stress Tester",
    version="2.0.0"
)

# Enable CORS for institutional development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files & Templates
STATIC_DIR = os.path.join(CURRENT_DIR, "src", "frontend", "static")
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "src", "frontend", "templates")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API Router
app.include_router(api_router)

@app.on_event("startup")
def startup_event():
    print("\n============================================================")
    print("[INIT] Initializing S&P Global x CRISIL Financial Risk Engine")
    print("============================================================")
    init_db()
    print("[OK] SQLite Database initialized at data/risk_engine.db")
    print("[OK] Pre-seeded accounts: admin (CRO) & analyst (Portfolio Manager)")
    print("[OK] Synthetic $1.04B Wholesale Portfolio active")
    print("[OK] Real-time Ingestion Connectors (CNBC, MarketWatch, WSJ) active")
    print("============================================================")
    print("[URL] Dashboard: http://localhost:8000")
    print("[URL] Swagger Docs: http://localhost:8000/docs")
    print("============================================================\n")

@app.get("/")
def serve_root(request: Request):
    """Entry point: institutional login and signup gateway."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login")
def serve_login(request: Request):
    """Institutional login and signup portal."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
def serve_dashboard(request: Request):
    """Serves the ISTC-style quantitative risk platform."""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
