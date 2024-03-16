import os
from typing import Union
from urllib.parse import urlparse

import redis
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from rq import Queue

# from .lib.aws_wrapper import upload_file
from .lib.aws_wrapper import download_file
from .lib.module_example import count_string_len

load_dotenv()

origins = ["http://localhost:3000"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.environ.get("REDISCLOUD_URL") is None:
    r = redis.Redis()
else:
    url = urlparse(os.environ.get("REDISCLOUD_URL"))
    r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
q = Queue(connection=r)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    result = q.enqueue(count_string_len, "This is a string")
    return result.get_id()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/uploadfile/")
async def create_upload_file(song: UploadFile):
    print(song)
    # upload_file(song.filename)
    return {"filename": song.filename}


@app.get("/download/{file_name}")
def get_download_file(file_name: str):
    return download_file(file_name)


@app.get("/string_len/{string}")
def string_len(string: str):
    job = q.enqueue(count_string_len, string)
    job_id = job.get_id()
    return RedirectResponse(f"/jobs/{job_id}/status")


@app.get("/jobs/{job_id}/status")
def job_status(job_id: str):
    job = q.fetch_job(job_id)
    if job is None:
        return "Job not found", 404
    return job.get_status(), 200
