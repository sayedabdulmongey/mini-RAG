from fastapi import APIRouter,Depends
from helpers import get_settings,Settings



base_router = APIRouter(
    prefix='/base',
    tags= ['Base']
)

@base_router.get("/")
async def welcome_func(app_settings:Settings = Depends(get_settings)):
    # app_settings = get_settings()  # Using Depends(get_settings) ensures that the get_settings function is called dynamically 
                                     # on each request, providing the most up-to-date settings. This also allows FastAPI to 
                                     # handle dependency injection automatically, making the code cleaner and easier to manage,
                                     # especially as the project scales and additional dependencies are introduced.

    
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "message": f"Welcome to {app_name}",
        "version": app_version
    }
