from fastapi import APIRouter, Depends, UploadFile, status, Request
# Request is used to acces the app that is initialized in main.py ( to access db_client and so on .. )

from fastapi.responses import JSONResponse
import os
from helpers import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal, ProjectModel, ChunkModel
import aiofiles
import logging
from .schemas import ProcessRequest
from models.db_schemas import DataChunk

logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(
    prefix='/base/data',
    tags=['Base', 'data']
)


@data_router.post("/upload/{project_id}")
async def upload_func(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    data_control = DataController()

    is_valid, response_signal, type = data_control.validate_uploaded_file(
        file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": response_signal,
                "type": type
            }
        )

    file_path, file_key = data_control.generate_unique_filepath(
        file, project_id)

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error in Uploading File {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            'file_key': file_key,
            # 'project_id': str(project.id)  # convert the ObjectId to string
        }
    )


@data_router.post("/process/{project_id}")
async def proccess_func(request: Request, project_id: str, process_request: ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunck_size
    overlap_len = process_request.overlap_size
    do_reset = process_request.do_reset

    process_controller = ProcessController(project_id)

    file_content = process_controller.get_file_content(file_id)

    chunks = process_controller.get_file_chunks(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_len=overlap_len
    )
    if len(chunks) == 0 or chunks is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.PROCESS_FAILED.value
            }
        )

    chunk_model = ChunkModel(
        db_client=request.app.db_client
    )

    if do_reset is True:
        _ = await chunk_model.delete_chunk_by_project_id(
            project_id=project_id
        )

    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    chunk_records = [
        DataChunk(
            project_id=project_id,
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=idx+1,
            chunk_project_id=project.id
        )
        for idx, chunk in enumerate(chunks)
    ]

    total_chunks = await chunk_model.insert_many_chunks(
        chunks=chunk_records
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.PROCESS_SUCCESS.value,
            'total_chunks': total_chunks
        }
    )
