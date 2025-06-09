from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

FT_TRAINED_MODEL_PATH = "./filter-model"
CLF_TRAINED_MODEL_PATH = "./classify-model"

MYSQL_HOST = "mysql-db"  # container name
MYSQL_PORT = 3306
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = "smki_capstone_db"

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

CHROMA_HOST = "chroma-db"  # container name
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = "capstone_0519"
