from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import Asset
from bson import ObjectId


class AssetModel(BaseDataModel):
    '''
    This class is the data model for the assets collection in the database
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSETS_NAME.value]

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
        indexes = Asset.get_indexes()
        if DataBaseEnum.COLLECTION_ASSETS_NAME.value not in all_collections:
            for index in indexes:
                await self.collection.create_index(
                    index['key'],
                    name=index['name'],
                    unique=index['unique']
                )

    async def create_asset(self, asset: Asset):

        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))

        asset.id = result.inserted_id

        return asset

    async def get_all_project_assets(self, project_id: str):
        return self.collection.find(
            {
                'asset_project_id': ObjectId(project_id) if isinstance(project_id, str) else project_id
            }
        ).to_list(length=None)  # to_list(length=None) length=None means return all the documents
