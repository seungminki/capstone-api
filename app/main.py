from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from app.routers import classify, filter, similar
from utils.s3_util import download_folder_from_s3
from settings import FT_TRAINED_MODEL_PATH, CLF_TRAINED_MODEL_PATH

description = """
CAPSTONE-API helps you do awesome stuff. 🚀
"""


def start():
    def load_model():
        download_folder_from_s3(
            s3_prefix="filtering/",  # s3://my-ml-models/checkpoints/
            local_dir=FT_TRAINED_MODEL_PATH,  # 로컬 저장 위치
        )

        download_folder_from_s3(
            s3_prefix="classification/",
            local_dir=CLF_TRAINED_MODEL_PATH,
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
