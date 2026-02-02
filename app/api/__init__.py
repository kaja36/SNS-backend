from fastapi import APIRouter
from .endpoints import users

api_router = APIRouter()

# APIのルーターを登録
api_router.include_router(users.router, prefix="/users", tags=["users"])