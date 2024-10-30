# fastapi_project/main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from utils.s3 import S3Client

app = FastAPI(
    title="Weed Lab API",
    description="An api to manipulate object storage or files on seaweedsFS properties",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "S3",
            "description": "Operations with object storage in common s3 SDK",
        },
        {"name": "DuckDB", "description": "Operations with duckdb on object storage"},
    ],
)
s3_client = S3Client()


@app.get("/")
async def read_root():
    return {"message": "Do you wanna cook?"}


@app.get("/s3/bucket", tags=["S3"])
async def read_s3_bucket():
    try:
        response = s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response]
        return JSONResponse(status_code=200, content={"data": buckets})
    except SystemError as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.post("/s3/bucket", tags=["S3"])
async def create_s3_bucket(bucket_name: str):
    try:
        s3_client.create_buckets(bucket_name=bucket_name)
        return JSONResponse(
            status_code=201,
            content={"message": "Successfully create {}".format(bucket_name)},
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.post("/s3/file", tags=["S3"])
async def upload_file_to_s3(
    bucket_name: str, file: UploadFile, s3_path: str | None = None
):
    try:
        file_name = file.filename
        s3_path = s3_path or file_name
        s3_client.update_file(file.file, bucket_name, s3_path)
        return JSONResponse(
            status_code=201,
            content={
                "message": "Successfully create file {} with path {} on bucket name {}".format(
                    file_name, s3_path, bucket_name
                )
            },
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


def start():
    uvicorn.run("weed_api.main:app", host="0.0.0.0", port=8000, reload=True)
