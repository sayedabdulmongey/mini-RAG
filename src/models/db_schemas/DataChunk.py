from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId


class DataChunk(BaseModel):
    '''
    DataChunk Class for the FastAPI Application
    In this class, we define the schema for the DataChunk collection in the MongoDB Database

    It has the following methods:
    get_indexes: This method returns the indexes for the DataChunk collection
    '''

    id: Optional[ObjectId] = Field(None, alias='_id')
    # i used alias to rename the id field to _id to avoid conflicts with the default id field in the MongoDB collection and the private id field in the DataChunk class

    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict

    # must be greater than 0 (gt == greater than)
    chunk_order: int = Field(..., gt=0)

    # this is the project id that the chunk belongs to related to _id in the project collection
    chunk_project_id: ObjectId

    chunk_asset_id: ObjectId

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                'key': [
                    ('chunk_project_id', 1)
                ],  # means use chunk_project_id as an index and 1 means >> sort it ascending
                'name': 'chunk_project_id_index_1',
                'unique': False  # multiple chunks may belong to the same project id
            }
        ]


class RetrievedDocument(BaseModel):
    '''
    RetrievedDocument Class for the FastAPI Application
    In this class, we define the schema for the RetrievedDocument object
    '''
    text: str
    score: float
    metadata: str
