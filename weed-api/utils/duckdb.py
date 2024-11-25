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

    def read_s3(self, bucket="", object_key="", extension="", output="json", limit=100):

        print(extension, output)
        if not extension in ["csv", "parq", "parquet", "json"]:
            raise Exception(
                "[S3 Error] the extension is not valid, please provide csv, parq, parquet, json"
            )

        if not output in ["json", "blob", "df"]:
            raise Exception(
                "[DuckDB Error] the output is not valid, please provide json, blob, df"
            )

        url = f"s3://{bucket}/{object_key}"

        try:

            buffer = io.BytesIO()
            read_query = f"""'{url}'"""

            if extension == "csv":
                read_query = f"""read_csv_auto('{url}')"""
            if extension == "parq" or extension == "parquet":
                read_query = f"""read_parquet('{url}')"""
            if extension == "json":
                read_query = f"""read_json_auto('{url}')"""

            query = f"SELECT * FROM {read_query}" + (
                "" if limit == None else f" LIMIT {limit};"
            )

            cursor = self.conn.execute(query)
            res = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]

            df = PL.DataFrame(res, schema=cols, strict=False)

            if output == "blob":
                df.write_parquet(buffer)
                return buffer

            if output == "df":
                return df

            if output == "json":
                return df.to_dicts()

        except Exception as error:
            logging.error("[DuckDB Error] read_s3 error: {}".format(error))
            raise Exception(error)

    def read_s3_schema(self, bucket="", object_key=""):

        url = f"s3://{bucket}/{object_key}"

        try:

            query = f"SELECT * FROM '{url}';"
            cursor = self.conn.execute(query)

            schema = [
                {"id": desc[0], "dt_type": desc[1].lower()} for desc in cursor.description
            ]
            return schema

        except Exception as error:
            logging.error("[DuckDB Error] query read_s3_schema error: {}".format(error))
            raise Exception(error)
