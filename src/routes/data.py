from fastapi import APIRouter, Depends, UploadFile, status, Request
# Request is used to acces the app that is initialized in main.py ( to access db_client and so on .. )

from fastapi.responses import JSONResponse
import os
from helpers import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal, ProjectModel, ChunkModel, AssetModel
import aiofiles
import logging
from .schemas import ProcessRequest
from models.db_schemas import DataChunk, Asset
from bson import ObjectId
from models.enums import AssetTypeEnum

logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(
    prefix='/base/data',
    tags=['Base', 'data']
)


@data_router.post("/upload/{project_id}")
async def upload_func(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(
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

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    asset = Asset(
        asset_project_id=project.id,
        asset_name=file_key,
        asset_type=AssetTypeEnum.FILE.value,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(
        asset=asset
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

    chunk_size = process_request.chunck_size
    overlap_len = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    process_controller = ProcessController(project_id)

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    project_file_ids = {}

    if process_request.file_id:
        asset_record = await asset_model.get_asset_by_id(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'signal': ResponseSignal.FILE_PROCESS_NOT_FOUND.value
                }
            )

        project_file_ids = {
            asset_record.id: asset_record.asset_name
        }
    else:
        project_asset_records = await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value
        )

        project_file_ids = {
            asset_record.id: asset_record.asset_name
            for asset_record in project_asset_records
        }

    if len(project_file_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.FILE_PROCESS_FAILED.value
            }
        )

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if do_reset is True:
        _ = await chunk_model.delete_chunk_by_project_id(
            project_id=project.id
        )

    total_files, total_chunks = 0, 0

    for asset_id, file_id in project_file_ids.items():

        file_content = process_controller.get_file_content(file_id)

        if file_content is None:
            logger.error(f"Error in processing file : {file_id}")
            continue

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

        chunk_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=idx+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for idx, chunk in enumerate(chunks)
        ]

        total_chunks += await chunk_model.insert_many_chunks(
            chunks=chunk_records
        )
        total_files += 1

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.PROCESS_SUCCESS.value,
            'total_chunks': total_chunks,
            'total_files': total_files
        }
    )
