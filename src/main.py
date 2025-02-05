from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
# this motor client is used to connect to the mongodb database
# perform operations on it (it is async and fast api is async so it is used to make the operations faster)

from stores.llm import LLMFactoryProvider
from stores.vectordb import VectorDBFactoryProvider

from helpers.config import get_settings
from contextlib import asynccontextmanager

from models import ProjectModel, ChunkModel


async def startup_spam():
    # this func is used to make the connection to the mongodb database
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DATABASE]

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


async def shutdown_spam():
    # this func is used to close the connection to the mongodb database
    app.mongo_conn.close()
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
