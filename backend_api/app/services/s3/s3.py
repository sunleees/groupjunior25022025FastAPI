import aioboto3
from fastapi import APIRouter, Body, UploadFile

ACCESS_KEY = "20196cefb5b98a43b02dd59e622b81e4"
SECRET_KEY = "0333783f261132bad7d985517ec8176abcd5c06db9e677b1c99b169413bedc46"
BUCKET_NAME = "group25022025"
ENDPOINT = (
    "https://f617d2ef7efe773c811bfd2127ade693.r2.cloudflarestorage.com/group25022025"
)
PUBLIC_URL = "https://pub-868f509dfcb24895838ff73db7650ffe.r2.dev"


class S3Storage:
    def __init__(self):
        self.bucket_name = BUCKET_NAME

    async def get_s3_session(self):
        session = aioboto3.Session()
        async with session.client(
            "s3",
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name="EEUR",
        ) as s3:
            yield s3

    async def upload_product_image(self, file: UploadFile, product_uuid: str) -> str:
        async for s3_client in self.get_s3_session():
            path = f"products/{product_uuid}/{file.filename}"
            await s3_client.upload_fileobj(file, self.bucket_name, path)
            url = f"{PUBLIC_URL}/{path}"
        return url


s3_storage = S3Storage()
