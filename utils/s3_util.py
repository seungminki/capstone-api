import boto3
import time
import os

from settings import AWS_S3_BUCKET_NAME, AWS_S3_KEY_ID, AWS_S3_SECRET_KEY


def download_file_from_s3(local_dir, local_filename, s3_key):

    local_path = os.path.join(local_dir, local_filename)

    if os.path.exists(local_path):
        print(f"already exists in '{local_dir}'")
        return

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_S3_KEY_ID,
        aws_secret_access_key=AWS_S3_SECRET_KEY,
        region_name="ap-northeast-2",
    )

    try:
        print(f"Downloading {s3_key} to {local_path} ...")
        s3.download_file(AWS_S3_BUCKET_NAME, s3_key, local_path)

    except Exception as e:
        print(f"Failed to download: {e}")


def download_folder_from_s3(s3_prefix, local_dir):
    if os.path.exists(local_dir):
        print(f"already exists in '{local_dir}'")
        return

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_S3_KEY_ID,
        aws_secret_access_key=AWS_S3_SECRET_KEY,
        region_name="ap-northeast-2",
    )

    response = s3.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME, Prefix=s3_prefix)

    if "Contents" not in response:
        print(f"No files found in s3://{AWS_S3_BUCKET_NAME}/{s3_prefix}")
        return

    start = time.time()

    for obj in response["Contents"]:
        s3_key = obj["Key"]

        if s3_key.endswith("/"):
            continue

        # 로컬 경로 생성
        relative_path = os.path.relpath(s3_key, s3_prefix)
        local_path = os.path.join(local_dir, relative_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        print(f"Downloading {s3_key} to {local_path} ...")
        s3.download_file(AWS_S3_BUCKET_NAME, s3_key, local_path)

    end = time.time()
    print(f"model download time: {end - start}.3f")
