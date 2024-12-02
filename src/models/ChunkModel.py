from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import DataChunk
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    '''
    ChunkModel class is the data model for the chunks collection in the database
    In this class, we have the following methods:
    - create_chunk: to insert a new chunk into the chunks collection
    - get_chunk: to retrieve a chunk from the chunks collection
    - insert_many_chunks: to insert multiple chunks into the chunks collection
    - delete_chunk_by_project_id: to delete all the chunks that belong to a project
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk):

        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        # by_alias=True: to use the alias name in the schema
        # exclude_unset=True: to exclude the fields that are not set in the schema which means the values that aren't provided in the project object will be equal to None
        # i do this because i solve problem with acces _id which is private attribute so i used alias to access it
        chunk._id = result.inserted_id

        return result

    async def get_chunk(self, chunk_id: str):

        result = await self.collection.find_one({
            '_id': chunk_id
        })

        if result is None:

            return None

        # Because the records is a dictionary, we need to convert it to a DataChunk object
        return DataChunk(**result)

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        '''
        In this method, we insert multiple chunks into the chunks collection
        Instead of inserting one by one, we insert in batches to improve the performance of the insertion which's name is bulk insertion
        '''

        for i in range(0, len(chunks), batch_size):

            batch = chunks[i:i+batch_size]

            operation = [
                InsertOne(chunk.dict(
                    by_alias=True, exclude_unset=True
                ))
                for chunk in batch
            ]

            await self.collection.bulk_write(operation)

        return len(chunks)

    async def delete_chunk_by_project_id(self, project_id: str):

        result = await self.collection.delete_many({
            'project_id': project_id
        })

        return result.deleted_count