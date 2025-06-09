from fastapi import APIRouter
from transformers import BertTokenizer

from utils.mysql_util import insert_posts, insert_categories
from utils.openai_util import openai_api
from utils.bert_util import BertForMultiLabelClassification, MultiLabelPredictor
from utils.preprocess import preprocess
from app.schemas import RequestData
from settings import CLF_TRAINED_MODEL_PATH

import json

router = APIRouter(prefix="/classify", tags=["classify"])


@router.post("")
def get_tagging_list(req: RequestData):
    # pred_category = openai_api(req.content)

    insert_posts(req)
    pred_category = predict(req.content)

    insert_categories(req, pred_category)

    return {
        "text": req.content,
        "pred_category": pred_category,
    }


def predict(text: str) -> list:
    text = preprocess(text)

    model = BertForMultiLabelClassification.from_pretrained(CLF_TRAINED_MODEL_PATH)
    tokenizer = BertTokenizer.from_pretrained(CLF_TRAINED_MODEL_PATH)

    with open(f"{CLF_TRAINED_MODEL_PATH}/labels.json", "r", encoding="utf-8") as f:
        labels = json.load(f)

    predictor = MultiLabelPredictor(
        model=model,
        tokenizer=tokenizer,
        label_names=labels,  # 예: ["연애", "취업", "감정", ...]
        threshold=0.5,
    )

    df = predictor.predict_from_texts([text], return_probs=True)

    pred_labels_binary = df.iloc[0][df.iloc[0] == 1].index.tolist()

    return ", ".join(pred_labels_binary)  # list to str
