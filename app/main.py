# app/main.py

from fastapi import FastAPI
from app.api.api_router import api_router
from app.core.config import settings

# --- ADD THIS LINE ---
# This forces SQLAlchemy to load and register all relationships in memory on startup
import app.models 

app = FastAPI(
    title="AI Resume Builder API",
    description="Automated ATS-friendly resume generation.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running securely."}