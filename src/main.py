from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
# this motor client is used to connect to the mongodb database and perform operations on it (it is async and fast api is async so it is used to make the operations faster)
from helpers.config import get_settings

app = FastAPI()

@app.on_event('startup')
async def startup_db_client():
    # this func is used to make the connection to the mongodb database
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DATABASE]

@app.on_event('shutdown')
async def shutdown_db_client():
    # this func is used to close the connection to the mongodb database
    app.mongo_conn.close()



app.include_router(base.base_router)
app.include_router(data.data_router)
