from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import DataChunk
from pymongo import InsertOne
from bson import ObjectId

from sqlalchemy.future import select
from sqlalchemy import func, delete


class ChunkModel(BaseDataModel):

    '''
    ChunkModel class is the data model for the chunks collection in the database
    The class is responsible for all the operations related to the chunks collection in the database
    The class inherits from the BaseDataModel class which is responsible for the database connection

    The class has the following methods:
    - create_instance: This method is used to create an instance of the ChunkModel class
    - create_chunk: This method is used to create a new chunk in the database
    - get_chunk: This method is used to get a chunk from the database by its id
    - insert_many_chunks: This method is used to insert multiple chunks into the database
    - delete_chunk_by_project_id: This method is used to delete all the chunks related to a project from the database
    - get_project_chunks: This method is used to get all the chunks related to a project from the database with pagination 
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def create_chunk(self, chunk: DataChunk):

        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            # This is to refresh the project object with the new values from the database
            await session.refresh(chunk)

        return chunk

    async def get_chunk(self, chunk_id: int):

        async with self.db_client() as session:
            # In execute method, we don't need to commit the transaction because we commit when we affect the database also for refresh
            # In execute method, we don't need to begin the session because the session will be started automatically
            query = select(DataChunk).where(
                DataChunk.chunk_id == chunk_id)
            result = await session.execute(query)
            chunk = result.scalar_one_or_none()
            return chunk

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        '''
        In this method, we insert multiple chunks into the chunks collection
        Instead of inserting one by one, we insert in batches to improve the performance of the insertion which's name is bulk insertion
        '''
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i+batch_size]
                    session.add_all(batch)
            await session.commit()

        return len(chunks)

    async def delete_chunk_by_project_id(self, project_id: int):

        async with self.db_client() as session:
            query = delete(DataChunk).where(
                DataChunk.chunk_project_id == project_id)
            result = await session.execute(query)
            await session.commit()

        return result.rowcount

    async def get_project_chunks(self, project_id: int, page_no: int = 1, page_size: int = 50):
        async with self.db_client() as session:

            query = select(DataChunk).where(
                DataChunk.chunk_project_id == project_id).offset((page_no-1)*page_size).limit(page_size)

            result = await session.execute(query)
            records = result.scalars().all()

        return records

    async def get_total_chunks_count(self, project_id: int):

        total_count = 0
        async with self.db_client() as session:
            query = select(func.count(DataChunk.chunk_id)).where(
                DataChunk.chunk_project_id == project_id)
            result = await session.execute(query)
            total_count = result.scalar()

        return total_count
