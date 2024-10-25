from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: str
    chunck_size: Optional[int] = 100
    overlap_size : Optional[int] = 10
    do_reset : Optional[bool] = False