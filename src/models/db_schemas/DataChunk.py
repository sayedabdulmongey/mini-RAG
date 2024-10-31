from pydantic import BaseModel,Field,validator
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    _id : Optional[ObjectId]

    project_id : str = Field(...,min_length=1)
    chunk_text : str = Field(...,min_length=1)
    chunk_metadata : dict
    chunk_order : int = Field(...,gt=0) # must be greater than 0 (gt == greater than)
    chunk_project_id : ObjectId # this is the project id that the chunk belongs to related to _id in the project collection


    class Config:
        arbitrary_types_allowed = True