from pydantic import BaseModel
from typing import Optional


class PushRequest(BaseModel):

    '''
    PushRequest Class for the FastAPI Application
    In this class, we define the schema for the Push Request for the FastAPI Application
    '''

    do_reset: Optional[bool] = False


class SearchRequest(BaseModel):

    '''
    SearchRequest Class for the FastAPI Application
    In this class, we define the schema for the Search Request for the FastAPI Application
    '''

    text: str
    limit: Optional[int] = 5
