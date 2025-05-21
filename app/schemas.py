from pydantic import BaseModel
from typing import Optional


class RequestData(BaseModel):
    post_id: int
    board_id: int
    content: Optional[str] = None
    user_id: int
