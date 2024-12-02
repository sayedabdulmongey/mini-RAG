from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):

    '''
    ProcessRequest Class for the FastAPI Application
    In this class, we define the schema for the Process Request for the FastAPI Application
    '''

    file_id: str
    chunck_size: Optional[int] = 100
    overlap_size: Optional[int] = 10
    do_reset: Optional[bool] = False
