from typing import BinaryIO

import boto3

from config import settings


class S3:
    s3_domain = f'https://{settings.S3_CUSTOM_DOMAIN}/'

    def __init__(self, bucket: str = None) -> None:
        self.region_name = settings.AWS_REGION
        self.cli = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region_name,
        )
        self.resource = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region_name,
        )
        self.bucket = bucket if bucket else settings.S3_BUCKET_NAME

    def upload_fileobj(
        self, file_object: bytes | BinaryIO, path_file: str, extra_args: dict = {}
    ):
        if not extra_args:
            extra_args = {'ACL': 'public-read'}
        self.cli.upload_fileobj(
            Fileobj=file_object, Bucket=self.bucket, Key=path_file, ExtraArgs=extra_args
        )
        return f'https://{self.bucket}.s3.amazonaws.com/{path_file}'

    def download_file(self, object_url, file_name):
        self.cli.download_file(self.bucket, object_url, file_name)

    def download_fileobj(self, object_url, file_name):
        self.cli.download_fileobj(self.bucket, object_url, file_name)

    def generate_presigned_url(
        self, object_url: str, cli_method: str = 'get_object', ttl: int = 1800
    ):
        object_url = object_url.replace(self.s3_domain, '')
        return self.cli.generate_presigned_url(
            ClientMethod=cli_method,
            Params={'Bucket': self.bucket, 'Key': object_url},
            ExpiresIn=ttl,
        )
