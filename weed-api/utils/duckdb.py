import os
import duckdb
import logging
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


class DuckDB:
    def __init__(
        self,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS,
        endpoint_url=S3_ENDPOINT_URL,
        region_name=S3_REGION,
    ):
        self.conn = duckdb.connect()
        self.conn.execute(
            f"""
                CREATE SECRET secret1 (
                TYPE S3,
                KEY_ID '{aws_access_key_id}',
                SECRET '{aws_secret_access_key}',
                REGION '{region_name}'
            );
            """
        )

        self.conn.execute("INSTALL httpfs")
        self.conn.execute("LOAD httpfs")


    def fetchSample(self, bucket, object_key):
        try:
            return self.conn.execute(
                f"""SELECT * FROM 's3://{bucket}/{object_key}' LIMIT 10"""
            )
        except Exception as err:
            print("err", err)
            return 200
