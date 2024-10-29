import os
import logging
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError



load_dotenv()

# Access environment variables
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_ENDPOINT_URL=os.environ.get("S3_ENDPOINT_URL")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


class S3Client:
    def __init__(self, aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_ACCESS, endpoint_url = S3_ENDPOINT_URL, region_name=S3_REGION):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            region_name=region_name
        )

    def create_buckets(self, bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as error:
            logging.error("[S3 Error] create bucket error: {}".format(error))
            return False
        return True
        
    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            return response["Buckets"]
        except ClientError as error:
            logging.error("[S3 Error] list buckets error: {}".format(error))
            raise Exception(error)

    def read_file(self, bucket_name, object_key):
        response = self.s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response["Body"].read()
        return content

    def delete_file(self, bucket_name, object_key):
        response = self.s3.delete_object(Bucket=bucket_name, Key=object_key)
        return response

    def update_file(self, bucket_name, object_key, data):
        response = self.s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        return response
