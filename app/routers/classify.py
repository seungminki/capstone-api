from fastapi import APIRouter
from utils.mysql_util import insert_posts, insert_categories
from utils.openai_util import openai_api
from app.schemas import RequestData

router = APIRouter(prefix="/classify", tags=["classify"])


@router.get("")
def get_tagging_list(req: RequestData):
    pred_category = openai_api(req.content)

    insert_posts(req)
    insert_categories(req, pred_category)

    return {
        "text": req.content,
        "pred_category": pred_category,
    }
