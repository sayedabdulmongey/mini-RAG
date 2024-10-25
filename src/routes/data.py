from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os
from helpers import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
from models import ResponseSignal
import aiofiles
import logging
from .schemas import ProcessRequest

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

@data_router.post("/process/{project_id}")
async def proccess_func(project_id:str,process_request:ProcessRequest):
    
    file_id = process_request.file_id
    chunk_size = process_request.chunck_size
    overlap_len = process_request.overlap_size

    process_controller = ProcessController(project_id)

    file_content = process_controller.get_file_content(file_id)

    chunks = process_controller.get_file_chunks(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_len=overlap_len
    )
    if len(chunks)==0 or chunks is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.PROCESS_FAILED.value
            }
        )

    return chunks










