from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os
from helpers import get_settings,Settings
from controllers import DataController,ProjectController
from models import ResponseSignal
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(
    prefix='/base/data',
    tags= ['Base','data']
)

@data_router.post("/upload/{project_id}")
async def upload_func(project_id:str,file:UploadFile,app_settings:Settings = Depends(get_settings)):
    

    data_control = DataController()

    is_valid,response_signal = data_control.validate_uploaded_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":response_signal
            }
        )
    
    file_path,file_key = data_control.generate_unique_filepath(file,project_id)

    try :
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error in Uploading File {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal':ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            'file_key':file_key
        }
    )




