from fastapi import FastAPI
from routes import base, data, nlp

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from stores.llm import LLMFactoryProvider
from stores.llm.templates import TemplateParser
from stores.vectordb import VectorDBFactoryProvider

from helpers.config import get_settings
from contextlib import asynccontextmanager

from models import ProjectModel, ChunkModel


async def startup_spam():

    settings = get_settings()

    postgres_url = f"postgresql+psycopg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"

    app.db_engine = create_async_engine(
        url=postgres_url,
    )

    app.db_client = sessionmaker(
        app.db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    llm_factory_provider = LLMFactoryProvider(config=settings)
    vectordb_factory_provider = VectorDBFactoryProvider(config=settings)

    # Project model
    app.project_model = await ProjectModel.create_instance(
        db_client=app.db_client
    )

    # Chunk model
    app.chunk_model = await ChunkModel.create_instance(
        db_client=app.db_client
    )

    # Generation model
    app.generation_model = llm_factory_provider.create_provider(
        provider=settings.GENERATION_BACKEND)
    app.generation_model.set_generation_model(
        model_id=settings.GENERATION_MODEL_ID)

    # Embedding model
    app.embedding_model = llm_factory_provider.create_provider(
        provider=settings.EMBEDDING_BACKEND)
    app.embedding_model.set_embedding_model(
        embedding_model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_SIZE)

    # VectorDB
    app.vectordb_client = vectordb_factory_provider.create_provider(
        provider=settings.VECTOR_DB_BACKEND
    )
    app.vectordb_client.connect()

    # Template parser
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANGUAGE,
        default_language=settings.DEFAULT_LANGUAGE
    )


async def shutdown_spam():

    await app.db_engine.dispose()
    app.vectordb_client.disconnect()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_spam()
    yield
    await shutdown_spam()


app = FastAPI(lifespan=lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
