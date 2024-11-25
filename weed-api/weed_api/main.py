# fastapi_project/main.py
import os
import uvicorn
import json
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from utils.s3 import S3Client
from utils.duckdb import DuckDB
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
duckDb_client = DuckDB()


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


@app.get("/s3/file/{bucket_name}", tags=["S3"])
async def get_s3_file(
    bucket_name: str, object_key: str, extension: str, output: str | None = "json"
):
    if output != "json" and output != "blob":
        raise HTTPException(
            status_code=400, detail="Output data should be json or blob"
        )
    try:
        response = s3_client.read_file(bucket_name, object_key, extension, output)
        if output == "blob":
            response.seek(0)
            return StreamingResponse(response)

        return JSONResponse(status_code=200, content=response)
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


@app.get("/s3/{bucket_name}/objects", tags=["S3"])
async def get_s3_objects(bucket_name: str, prefix: str | None = ""):
    try:
        _prefix = prefix
        if _prefix:
            last_txt = _prefix.strip().split("/")[-1]
            if not last_txt.endswith("/"):
                _prefix = _prefix + "/"
        response = s3_client.list_objects(bucket_name, _prefix)
        return JSONResponse(status_code=200, content=response)
    except Exception as err:
        raise HTTPException(status_code=500, detail="S3 Error, {}".format(err))


###################################### DuckDB API ######################################


@app.get("/duckdb/s3", tags=["DuckDB"])
async def get_duckdb(
    bucket_name: str,
    object_key: str,
    extension: str | None,
    output: str | None = "json",
    limit=1,
):
    try:
        response = duckDb_client.read_s3(
            bucket_name, object_key, extension, output, limit
        )

        if output == "blob":
            response.seek(0)
            return StreamingResponse(response)
        dt = json.dumps(response)
        return JSONResponse(status_code=200, content=response)
    except Exception as err:
        raise HTTPException(status_code=500, detail="DuckDB Error, {}".format(err))


@app.get("/duckdb/s3/schema", tags=["DuckDB"])
async def get_duckdb_schema(
    bucket_name: str,
    object_key: str,
):
    try:
        response = duckDb_client.read_s3_schema(bucket_name, object_key)
        return JSONResponse(status_code=200, content=response)
    except Exception as err:
        raise HTTPException(status_code=500, detail="DuckDB Error, {}".format(err))


def start():
    uvicorn.run("weed_api.main:app", host="0.0.0.0", port=8000, reload=True)
