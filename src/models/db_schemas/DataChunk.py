from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId


class DataChunk(BaseModel):
    '''
    DataChunk Class for the FastAPI Application
    In this class, we define the schema for the DataChunk collection in the MongoDB Database
    '''

    id: Optional[ObjectId] = Field(None, alias='_id')
    # i used alias to rename the id field to _id to avoid conflicts with the default id field in the MongoDB collection and the private id field in the DataChunk class

    project_id: str = Field(..., min_length=1)
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict

    # must be greater than 0 (gt == greater than)
    chunk_order: int = Field(..., gt=0)

    # this is the project id that the chunk belongs to related to _id in the project collection
    chunk_project_id: ObjectId

    class Config:
        arbitrary_types_allowed = True
