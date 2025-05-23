from fastapi import APIRouter

from app.schemas import RequestData
from utils.mysql_util import insert_posts
from utils.chroma_util import search_similar

router = APIRouter(prefix="/similarity", tags=["similarity"])


@router.get("")
def get_similarity(req: RequestData):

    insert_posts(req)

    rows = search_similar(req.content)

    return {"content": req.content, "rows": rows}
