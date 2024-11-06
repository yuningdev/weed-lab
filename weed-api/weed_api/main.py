# fastapi_project/main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from utils.s3 import S3Client
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = S3Client()

class S3RequestBody(BaseModel):
    bucket_name: str


@app.get("/")
async def read_root():
    return {"message": "Do you wanna cook?"}


@app.get("/s3/buckets", tags=["S3"])
async def get_s3_buckets():
    try:
        response = s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response]
        return JSONResponse(status_code=200, content={"data": buckets})
    except SystemError as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.post("/s3/buckets", tags=["S3"])
async def create_s3_buckets(item: S3RequestBody):
    try:
        s3_client.create_buckets(item.bucket_name)
        return JSONResponse(
            status_code=201,
            content={"message": "Successfully create {}".format(item.bucket_name)},
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.delete("/s3/buckets", tags=["S3"])
async def delete_s3_buckets(item: S3RequestBody):
    try:
        s3_client.delete_buckets(item.bucket_name)
        return JSONResponse(
            status_code=201,
            content={"message": "Successfully delete {}".format(item.bucket_name)},
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.post("/s3/file", tags=["S3"])
async def upload_file_to_s3(
    bucket_name: str, file: UploadFile, object_key: str | None = None
):
    try:
        file_name = file.filename
        object_key = object_key or file_name
        s3_client.update_file(file.file, bucket_name, object_key)
        return JSONResponse(
            status_code=201,
            content={
                "message": "Successfully create file {} with path {} on bucket name {}".format(
                    file_name, object_key, bucket_name
                )
            },
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.get("/s3/{bucket_name}/objects", tags=["S3"])
async def get_s3_objects(bucket_name: str, prefix: str | None = ""):
    try:
        response = s3_client.list_objects(bucket_name, prefix)
        return JSONResponse(status_code=200, content=response)
    except SystemError as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


def start():
    uvicorn.run("weed_api.main:app", host="0.0.0.0", port=8000, reload=True)
