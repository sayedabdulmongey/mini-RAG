from fastapi import APIRouter
import os


base_router = APIRouter(
    prefix='/base',
    tags= ['Base']
)

@base_router.get("/")
def welcome_func():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "message": f"Welcome to {app_name}",
        "version": app_version
    }
