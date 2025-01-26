from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId
from datetime import datetime


class Asset(BaseModel):

    '''
    Asset Class for the FastAPI Application
    In this class, we define the schema for the Asset collection in the MongoDB Database

    It has the following methods:
    get_indexes: This method returns the indexes for the Asset collection

    '''

    id: Optional[ObjectId] = Field(None, alias='_id')
    asset_project_id: ObjectId
    asset_name: str = Field(..., min_length=1)
    asset_type: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(default=None)
    asset_pushed_at: str = Field(default=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("asset_project_id", 1)
                ],  # means use project_id as an index and 1 means >> sort it ascending
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],  # means use project_id as an index and 1 means >> sort it ascending
                "name": "asset_project_id_name_index_1",
                "unique": True
            },
        ]
