from fastapi import APIRouter
from app.api import users

api_router = APIRouter()

# Register the users router under the /users path
api_router.include_router(users.router, prefix="/users", tags=["Users"])
