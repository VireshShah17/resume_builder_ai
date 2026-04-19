from fastapi import FastAPI
from app.api.v1.api_router import api_router
from app.core.config import settings

app = FastAPI(
    title="AI Resume Builder API",
    description="Automated ATS-friendly resume generation.",
    version="1.0.0"
)

# Include the main API router
# app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running securely."}