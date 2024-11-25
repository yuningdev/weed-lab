import os
import io
import duckdb
import logging
from dotenv import load_dotenv
import polars as PL


load_dotenv()

# Access environment variables
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")
DUCKDB_S3_URLSTYLE = os.environ.get("DUCKDB_S3_URLSTYLE", "vhost")

API_STAGE = os.environ.get("API_STAGE", "dev")


class DuckDB:
    def __init__(
        self,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS,
        endpoint_url=S3_ENDPOINT_URL,
        region_name=S3_REGION,
    ):

        duckdb.execute("INSTALL httpfs")
        duckdb.execute("LOAD httpfs")
        self.conn = duckdb.connect(database=":memory:", read_only=False)
        self.conn.execute(
            f"""
                CREATE SECRET secret1 (
                TYPE S3,
                KEY_ID '{aws_access_key_id}',
                SECRET '{aws_secret_access_key}',
                ENDPOINT '{endpoint_url.replace(
                        'http://' if API_STAGE == 'dev' else 'https://', ""
                    )}',
                USE_SSL '{API_STAGE != 'dev'}',
                REGION '{region_name}',
                URL_STYLE 'path'
            );
            """
        )

    def read_s3(self, bucket="", object_key="", output="json", limit=100):

        if not output in ["json", "blob", "df"]:
            raise Exception(
                "[DuckDB Error] the output is not valid, please provide json, blob, df"
            )
        
    
        url = f"s3://{bucket}/{object_key}"

        try:


            buffer = io.BytesIO()
            query = f"SELECT * FROM '{url}'" + ("" if limit == None else f" LIMIT {limit};")
            res = self.conn.execute(query).fetchall()

            df = PL.DataFrame(res, strict=False)

            print(df.head())

            if output == "blob":
                duckdb.from_df(df).to_parquet(buffer)
                return buffer

            if output == "df":
                return df

            if output == "json":
                return df.to_dicts()

        except Exception as error:
            logging.error("[DuckDB Error] query s3 error: {}".format(error))
            raise Exception(error)
