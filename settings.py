from dotenv import load_dotenv
import os

load_dotenv()

AWS_S3_BUCKET_NAME = os.getenv("aws_s3_bucket_name")
AWS_S3_KEY_ID = os.getenv("aws_s3_id")
AWS_S3_SECRET_KEY = os.getenv("aws_s3_key")

TRAINED_MODEL_PATH = "./filter-model"

MYSQL_HOST = "mysql-db"  # container name
MYSQL_PORT = 3306
MYSQL_USER = os.getenv("mysql_user")
MYSQL_PASSWORD = os.getenv("mysql_password")

OPENAI_TOKEN = os.getenv("openai_token")

CHROMA_HOST = "chroma-db"  # container name
CHROMA_PORT = 8000
CHROMA_COLLECTION_NAME = "capstone_0519"
