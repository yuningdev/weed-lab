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
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


class S3Client:
    def __init__(
        self,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS,
        endpoint_url=S3_ENDPOINT_URL,
        region_name=S3_REGION,
    ):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
        )

    def create_buckets(self, bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as error:
            logging.error("[S3 Error] create bucket error: {}".format(error))
            return False
        return True

    def check_bucket_exist(self, bucket_name):
        # Not execute upload file if bucket not found
        try:
            self.s3.head_bucket(Bucket=bucket_name)
        except Exception as error:
            return False
        return True

    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            return response["Buckets"]
        except ClientError as error:
            logging.error("[S3 Error] list buckets error: {}".format(error))
            raise Exception(error)

    def delete_buckets(self, bucket_name):

        if not self.check_bucket_exist(bucket_name):
            raise Exception(f"[S3 Error] bucket {bucket_name} not exists")

        try:
            self.s3.delete_bucket(Bucket=bucket_name)
        except ClientError as error:
            logging.error("[S3 Error] delete buckets error: {}".format(error))
            return False
        return True

    def update_file(self, file, bucket_name, object_key):

        if not self.check_bucket_exist(bucket_name):
            raise Exception(f"[S3 Error] bucket {bucket_name} not exists")

        try:
            self.s3.upload_fileobj(file, bucket_name, object_key)

        except ClientError as error:
            logging.error("[S3 Error] upload file error: {}".format(error))
            return False
        return True

    # This function will return head dir folder or file based on the bucket and object prefix
    def list_objects(self, bucket_name, prefix):
        try:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
            paginator = self.s3.get_paginator("list_objects_v2")
            operation_parameters = {"Bucket": bucket_name, "Prefix": prefix}
            page_iterator = paginator.paginate(**operation_parameters)

            first_level_update_time = {}

            for page in page_iterator:

                if "Contents" in page:
                    for obj in page["Contents"]:
                        key = obj["Key"]
                        if "/" in key:
                            dir = key.strip("/").split("/")[0]

                            if dir in first_level_update_time:
                                if (
                                    obj["LastModified"]
                                    >= first_level_update_time[dir]["LastModified"]
                                ):
                                    first_level_update_time[dir] = obj
                            else:
                                first_level_update_time[dir] = obj

                        else:
                            first_level_update_time[key] = obj

            response = [
                {
                    **item,
                    "Key": item["Key"].split("/")[0],
                    "LastModified": item["LastModified"].strftime("%Y-%m-%d %H:%M:%S"),
                }
                for item in first_level_update_time.values()
            ]

            return response

        except ClientError as error:
            logging.error("[S3 Error] list object error: {}".format(error))
            return []
