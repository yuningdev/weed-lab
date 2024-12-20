import os
import io
import polars as PL
import logging
import re
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


def is_valid_bucket_name(bucket_name):
    # Basic regex for common constraints:
    regex = r"^[a-z0-9.-]{1,255}$"
    return re.match(regex, bucket_name) is not None


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
            if is_valid_bucket_name(bucket_name):
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                raise Exception("Invalid bucket name")
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
                        key = obj["Key"].replace(prefix, "")
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
                    "Id": item["Key"].replace(prefix, "").split("/")[0],
                    "LastModified": item["LastModified"].strftime("%Y-%m-%d %H:%M:%S"),
                }
                for item in first_level_update_time.values()
            ]

            return response

        except ClientError as error:
            logging.error("[S3 Error] list object error: {}".format(error))
            return []

    def read_file(self, bucket_name, object_key, extension, output="json"):
        if not extension in ["csv", "parq", "parquet", "json"]:
            raise Exception(
                "[S3 Error] the extension is not valid, please provide csv, parq, parquet, json"
            )

        if not output in ["json", "blob", "df"]:
            raise Exception(
                "[S3 Error] the output is not valid, please provide json, blob, df"
            )

        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=object_key)
            streaming_data = response["Body"].read()

            # The streaming data is empty binary b''
            if not streaming_data:
                return

            buffer = io.BytesIO(streaming_data)

            if output == "blob":
                return buffer

            df = PL.DataFrame()

            if extension == "csv":
                df = PL.read_csv(buffer)

            if extension == "parq" or extension == "parquet":
                df = PL.read_parquet(buffer)

            if output == "df":
                return df
            else:
                return df.to_dicts()

        except ClientError as error:
            print("error", error)

            logging.error("[S3 Error] read file error: {}".format(error))
            # raise Exception(error)
