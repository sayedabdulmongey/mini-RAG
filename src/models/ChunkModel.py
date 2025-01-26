from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import DataChunk
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    '''
    ChunkModel class is the data model for the chunks collection in the database
    The class is responsible for all the operations related to the chunks collection in the database
    The class inherits from the BaseDataModel class which is responsible for the database connection

    The class has the following methods:
    - create_instance: This method is used to create an instance of the ChunkModel class and initialize the collections with the indexes
    - init_collections: This method is used to initialize the collections in the database
    - create_chunk: This method is used to create a new chunk in the database
    - get_chunk: This method is used to get a chunk from the database by its id
    - insert_many_chunks: This method is used to insert multiple chunks into the database
    - delete_chunk_by_project_id: This method is used to delete all the chunks related to a project from the database
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        '''
        I created this method because i want to call async method (init_collections) in the init but its not allowed to call async method in the init because its not awaitable
        So i created this method to call the init method and the async method also 
        '''
        instance = cls(db_client)
        await instance.init_collections()
        return instance

    async def init_collections(self):
        '''
        This method is used to initialize the collections in the database
        The Initialization includes creating the indexes for the collections for the first time only
        '''
        all_collections = await self.db_client.list_collection_names()
        indexes = DataChunk.get_indexes()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:

            for index in indexes:
                await self.collection.create_index(
                    index['key'],
                    name=index['name'],
                    unique=index['unique']
                )

    async def create_chunk(self, chunk: DataChunk):

        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        # by_alias=True: to use the alias name in the schema
        # exclude_unset=True: to exclude the fields that are not set in the schema which means the values that aren't provided in the project object will be equal to None
        # i do this because i solve problem with acces _id which is private attribute so i used alias to access it
        chunk.id = result.inserted_id

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
            'chunk_project_id': project_id
        })

        return result.deleted_count
