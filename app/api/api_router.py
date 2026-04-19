from fastapi import APIRouter
from app.api import users, resumes

api_router = APIRouter()

# Register the users router under the /users path
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])