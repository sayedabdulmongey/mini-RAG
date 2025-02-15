from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemas import Asset
from bson import ObjectId

from sqlalchemy.future import select


class AssetModel(BaseDataModel):
    '''
    This class is the data model for the assets collection in the database

    It has the following methods:
    - create_instance: This method is a class method that creates an instance of the AssetModel class 
    - create_asset: This method is an async method that creates a new asset in the database
    - get_all_project_assets: This method is an async method that retrieves all the assets for a specific project
    - get_asset_by_id: This method is an async method that retrieves an asset by its id
    '''

    def __init__(self, db_client: object):
        super().__init__(db_client)

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def create_asset(self, asset: Asset):

        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            # This is to refresh the project object with the new values from the database
            await session.refresh(asset)
        return asset

    async def get_all_project_assets(self, asset_project_id: int, asset_type: str):
        async with self.db_client() as session:
            query = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_type == asset_type
            )
            result = await session.execute(query)
            records = result.scalars().all()

        return records

    async def get_asset_by_id(self, asset_project_id: int, asset_name: str):
        async with self.db_client() as session:
            query = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_name == asset_name
            )
            result = await session.execute(query)
            record = result.scalar_one_or_none()

        return record
