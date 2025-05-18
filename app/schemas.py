from pydantic import BaseModel
from typing import Optional


class PostRequest(BaseModel):
    post_id: int
    board_id: int
    content: Optional[str] = None
    user_id: Optional[int] = None
    tag: Optional[int] = None


class RequestData(BaseModel):
    post_id: Optional[str] = None
    board_id: Optional[str] = None
    content: Optional[str] = None
    user_id: Optional[int] = None


class ClfRequest(BaseModel):
    user_id: int
    is_required_tag: Optional[str] = None
    is_optional_tag: Optional[str] = None
