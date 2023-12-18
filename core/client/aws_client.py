import os
import boto3

from core.config.var_config import IS_PROD, S3_REGION, S3_BUCKET_NAME


class S3Client:
    if IS_PROD:
        s3 = boto3.client(
            service_name="s3",
            aws_access_key_id=os.environ.get("AWS_S3_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_S3_SECRET_ACCESS_KEY"),
        )
    else:
        from core.config import secrets

        s3 = boto3.client(
            service_name="s3",
            aws_access_key_id=secrets.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=secrets.AWS_S3_PRIVATE_KEY,
        )

    # Singleton
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(S3Client, cls).__new__(cls)
        return cls.instance

    def upload_fileobj(self, file, key: str = "", bucket_name: str = S3_BUCKET_NAME):
        return self.s3.upload_fileobj(file, bucket_name, key)

    def get_object(self, key: str, bucket_name: str = S3_BUCKET_NAME):
        return self.s3.get_object(Bucket=bucket_name, Key=key)

    def delete_object(self, key: str, bucket_name: str = S3_BUCKET_NAME):
        return self.s3.delete_object(Bucket=bucket_name, Key=key)

    @classmethod
    def get_object_url(self, key: str, bucket_name: str = S3_BUCKET_NAME) -> str:
        return f"https://{bucket_name}.s3.{S3_REGION}.amazonaws.com/{key}"
