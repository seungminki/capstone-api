from fastapi import FastAPI, BackgroundTasks
from app.routers import hatespeech
from utils.s3_util import download_folder_from_s3

description = """
CAPSTONE-2025 API helps you do awesome stuff. 🚀

1. content-similarity (cs)
2. hate-speech-detection (hd)
3. topic-classification (tc)

"""

app = FastAPI(
    title="Capstone-2025",
    description=description,
    summary="에브리타임 자동화 시스템 API",
    version="0.0.1",
)


@app.on_event("startup")
def load_model():
    download_folder_from_s3(
        s3_prefix="hate-speech/250518/model",  # s3://my-ml-models/checkpoints/
        local_dir="./hate-speech-model",  # 로컬 저장 위치
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(hatespeech.router)
