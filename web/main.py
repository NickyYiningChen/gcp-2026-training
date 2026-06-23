"""FastAPI application entry point for GCP 2026 Training Web App."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"

app = FastAPI(title="GCP 2026 Training", version="1.0.0")

# Template engine (must be set before routes that use it)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR), cache_size=0)
app.state.templates = templates

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Mount article scene images (separate dir outside web/static)
from web.config import ARTICLES_DIR
IMAGES_DIR = ARTICLES_DIR / "images"
app.mount("/article-images", StaticFiles(directory=str(IMAGES_DIR)), name="article_images")

# Import and register route modules
from web.routes.entry import router as entry_router
from web.routes.learn import router as learn_router
from web.routes.quiz import router as quiz_router
from web.routes.exam import router as exam_router
from web.routes.cert import router as cert_router


app.include_router(entry_router, prefix="", tags=["entry"])
app.include_router(learn_router, prefix="/learn", tags=["learn"])
app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
app.include_router(exam_router, prefix="/exam", tags=["exam"])
app.include_router(cert_router, prefix="/cert", tags=["cert"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def verify_files():
    """Verify all required files exist on startup."""
    from web.config import (ARTICLES_DIR, BANK_PATH, DIFF_GUIDE_PATH,
                            CURRICULUM_DIR, SCRIPTS_DIR)
    import json

    issues = []

    # Check articles
    for i in range(1, 55):
        f = ARTICLES_DIR / f"article-{i:02d}.md"
        if not f.exists():
            issues.append(f"Missing: {f}")

    # Check bank
    if not BANK_PATH.exists():
        issues.append(f"Missing: {BANK_PATH}")
    else:
        with open(BANK_PATH, encoding="utf-8") as f:
            bank = json.load(f)
        count = len(bank.get("questions", []))
        print(f"✅ Question bank loaded: {count} questions")

    # Check diff guide
    if not DIFF_GUIDE_PATH.exists():
        issues.append(f"Missing: {DIFF_GUIDE_PATH}")

    # Check curriculum
    if not CURRICULUM_DIR.exists():
        issues.append(f"Missing: {CURRICULUM_DIR}")

    # Check scripts
    pick_q = SCRIPTS_DIR / "pick_questions.py"
    make_cert = SCRIPTS_DIR / "make_certificate.py"
    if not pick_q.exists():
        issues.append(f"Missing: {pick_q}")
    if not make_cert.exists():
        issues.append(f"Missing: {make_cert}")

    if issues:
        print("⚠️  WARNING: Some files missing:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ All required files verified")

    print("🌐 GCP 2026 Training ready at http://localhost:8000")
