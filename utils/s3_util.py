import boto3
import time
import os

from settings import AWS_S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def download_file_from_s3(local_dir, local_filename, s3_key):

    local_path = os.path.join(local_dir, local_filename)

    if os.path.exists(local_path):
        print(f"already exists in '{local_dir}'")
        return

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )

    try:
        print(f"Downloading {s3_key} to {local_path} ...")
        s3.download_file(AWS_S3_BUCKET_NAME, s3_key, local_path)

    except Exception as e:
        print(f"Failed to download: {e}")


def download_folder_from_s3(s3_prefix: str, local_dir):
    if os.path.exists(local_dir):
        print(f"already exists in '{local_dir}'")
        return

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )

    latest_folder_name = get_latest_s3_folder(s3_prefix) # "filtering/"
    s3_prefix_datetime = f"{s3_prefix}{latest_folder_name}/model/" # "filtering/20250518_235959/model/"

    response = s3.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME, Prefix=s3_prefix_datetime)

    if "Contents" not in response:
        print(f"No files found in s3://{AWS_S3_BUCKET_NAME}/{s3_prefix_datetime}")
        return

    start = time.time()

    for obj in response["Contents"]:
        s3_key = obj["Key"]

        if s3_key.endswith("/"):
            continue

        # 로컬 경로 생성
        relative_path = os.path.relpath(s3_key, s3_prefix_datetime)
        local_path = os.path.join(local_dir, relative_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        print(f"Downloading {s3_key} to {local_path} ...")
        s3.download_file(AWS_S3_BUCKET_NAME, s3_key, local_path)

    end = time.time()
    print(f"Model Download Time: {end - start:.3f}")

def get_latest_s3_folder(s3_prefix: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )
    
    response = s3.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME, Prefix=s3_prefix)
    
    folder_names = set()
    
    for obj in response.get("Contents", []):
        key = obj['Key']  # ex: checkpoints/20240609_091500/model.pt
        relative_path = key.replace(s3_prefix, '')  # → 20240609_091500/model.pt
        parts = relative_path.split('/')
        if len(parts) > 1:
            folder_names.add(parts[0])  # → 20240609_091500
    
    if not folder_names:
        raise ValueError("No timestamp folders found under prefix.")

    # 문자열 기준 정렬 (timestamp 포맷이므로 정렬 시 최신이 마지막)
    latest_folder = sorted(folder_names)[-1]

    return latest_folder