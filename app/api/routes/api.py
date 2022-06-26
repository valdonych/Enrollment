from fastapi import APIRouter

from app.api.routes import import_api, nodes_api, delete_api

login_api_router = APIRouter()


login_api_router.include_router(delete_api.router)
login_api_router.include_router(nodes_api.router)
login_api_router.include_router(import_api.router)

