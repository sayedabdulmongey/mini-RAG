from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm import LLMFactoryProvider
# this motor client is used to connect to the mongodb database
# perform operations on it (it is async and fast api is async so it is used to make the operations faster)

from helpers.config import get_settings
from contextlib import asynccontextmanager


async def startup_db_client():
    # this func is used to make the connection to the mongodb database
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DATABASE]

    llm_factory_provider = LLMFactoryProvider(config=settings)

    # generation model
    app.generation_model = llm_factory_provider.create_provider(
        provider=settings.GENERATION_BACKEND)
    app.generation_model.set_generation_model(
        model_id=settings.GENERATION_MODEL_ID)

    # embedding model
    app.embedding_model = llm_factory_provider.create_provider(
        provider=settings.EMBEDDING_BACKEND)
    app.embedding_model.set_embedding_model(
        embedding_model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_SIZE)


async def shutdown_db_client():
    # this func is used to close the connection to the mongodb database
    app.mongo_conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client()
    yield
    await shutdown_db_client()


app = FastAPI(lifespan=lifespan)

# app.router.lifespan.on_startup.append(startup_db_client)
# app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)
