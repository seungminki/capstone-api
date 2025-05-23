from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from app.routers import classify, filter, similar
from utils.s3_util import download_folder_from_s3
from settings import TRAINED_MODEL_PATH

description = """
CAPSTONE-2025 API helps you do awesome stuff. 🚀

1. content-similarity: similarity
2. hate-speech-detection: filter
3. topic-classification: classification

"""


def start():
    def load_model():
        download_folder_from_s3(
            s3_prefix="hate-speech/250518/model",  # s3://my-ml-models/checkpoints/
            local_dir=TRAINED_MODEL_PATH,  # 로컬 저장 위치
        )

    print("Service is starting....")
    load_model()


def shutdown():
    print("Service is shutting down...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    start()

    yield

    # When service is stopped.
    shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="Capstone-2025",
    description=description,
    summary="에브리타임 자동화 시스템 API",
    version="0.0.1",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}


app.include_router(filter.router)
app.include_router(classify.router)
app.include_router(similar.router)
