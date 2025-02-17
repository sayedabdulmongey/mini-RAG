from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

import logging

from .schemas import PushRequest, SearchRequest

from controllers import NLPController
from models.enums import ResponseSignal


logger = logging.getLogger('uvicorn.error')


nlp_router = APIRouter(
    prefix='/base/nlp',
    tags=['Base', 'nlp']
)


# nlp_index_push
@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: int, push_request: PushRequest):

    project = await request.app.project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_model=request.app.generation_model,
        embedding_model=request.app.embedding_model,
        template_parser=request.app.template_parser
    )

    has_records = True
    inserted_chunks = 0
    ids = 0
    page_no = 1

    while has_records:

        chunks = await request.app.chunk_model.get_project_chunks(
            project_id=project.project_id,
            page_no=page_no
        )
        if chunks:
            page_no += 1

        if not chunks or len(chunks) == 0:
            has_records = False
            break

        chunk_ids = list(range(ids, ids+len(chunks)))
        ids += len(chunks)

        is_inserted = nlp_controller.index_into_vector_db(
            project_id=project_id,
            chunks=chunks,
            chunk_ids=chunk_ids,
            do_reset=push_request.do_reset
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'signal': ResponseSignal.CHUNK_INSERTION_TO_VECTORDB_FAILED.value
                }
            )

        inserted_chunks += len(chunks)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.CHUNK_INSERTION_TO_VECTORDB_SUCCESS.value,
            'inserted_chunks': inserted_chunks
        }
    )


# nlp_index_info
@nlp_router.get("/index/info/{project_id}")
async def index_info_project(request: Request, project_id: int):

    project = await request.app.project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_model=request.app.generation_model,
        embedding_model=request.app.embedding_model,
        template_parser=request.app.template_parser
    )

    collection_info = nlp_controller.get_vector_db_info(
        project_id=project_id
    )

    if not collection_info:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.GET_COLLECTION_INFO_FAILED.value
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.GET_COLLECTION_INFO_SUCCESS.value,
            'collection_info': collection_info
        }
    )


# nlp_index_search
@nlp_router.post("/index/search/{project_id}")
async def index_search_project(request: Request, project_id: int, search_request: SearchRequest):

    project = await request.app.project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_model=request.app.generation_model,
        embedding_model=request.app.embedding_model,
        template_parser=request.app.template_parser
    )

    results = nlp_controller.search_vector_db_collection(
        project_id=project_id,
        text=search_request.text,
        limit=search_request.limit
    )

    if not results:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.VECTORDB_SEARCH_ERROR.value
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
            'results': [
                result.dict()
                for result in results
            ]
        }
    )


# nlp_index_answer
@nlp_router.post("/index/answer/{project_id}")
async def index_answer_project(request: Request, project_id: int, search_request: SearchRequest):

    project = await request.app.project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_model=request.app.generation_model,
        embedding_model=request.app.embedding_model,
        template_parser=request.app.template_parser
    )

    full_prompt, chat_history, answer = nlp_controller.answer_rag_question(
        project_id=project_id,
        query=search_request.text,
        limit=search_request.limit
    )

    if not answer:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponseSignal.RAG_ANSWER_ERROR.value
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'signal': ResponseSignal.RAG_ANSWER_SUCCESS.value,
            'answer': answer,
            'full_prompt': full_prompt,
            'chat_history': chat_history
        }
    )
