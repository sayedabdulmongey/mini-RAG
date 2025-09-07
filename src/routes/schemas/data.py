from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):

    '''
    ProcessRequest Class for the FastAPI Application
    In this class, we define the schema for the Process Request for the FastAPI Application
    '''

    file_id: str = None
    chunk_size: Optional[int] = 1024
    overlap_size: Optional[int] = 205
    do_reset: Optional[bool] = False
