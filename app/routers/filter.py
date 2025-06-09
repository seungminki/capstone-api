from fastapi import APIRouter
from app.schemas import RequestData
from utils.mysql_util import insert_posts
from utils.preprocess import preprocess
from settings import FT_TRAINED_MODEL_PATH

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

router = APIRouter(prefix="/filter", tags=["filter"])


@router.post("")
def get_negative_score(req: RequestData):
    insert_posts(req)
    return predict(text=req.content)


def predict(text: str):
    text = preprocess(text)

    model = AutoModelForSequenceClassification.from_pretrained(FT_TRAINED_MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(FT_TRAINED_MODEL_PATH)

    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=128
    )
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs).item()
        # 둘 중 확률이 더 높은 쪽을 출력
        threshold = 0.7
        is_abusive_prob = probs[0][1].item()  # 클래스 1 = 비방글 확률

    return {
        "text": text,
        "is_abusive": is_abusive_prob > threshold,
        "probability": is_abusive_prob,
    }
