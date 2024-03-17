from typing import Union

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from .lib.aws_wrapper import download_file, upload_file_obj
from .lib.module_example import count_string_len
from .lib.queue_wrapper import enqueue_job, get_job_status

origins = ["http://localhost:3000"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    result = enqueue_job(count_string_len, "This is a string")
    return result.get_id()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/uploadfile/")
async def create_upload_file(song: UploadFile):
    try:
        upload_file_obj(song.file, song.filename)
    except Exception as e:
        return {"error": str(e)}
    return {"filename": song.filename}


@app.get("/download/{file_name}")
def get_download_file(file_name: str):
    return download_file(file_name)


@app.get("/string_len/{string}")
def string_len(string: str):
    job_id = enqueue_job(count_string_len, string)
    print(job_id)
    return RedirectResponse(f"/jobs/{job_id}/status")


@app.get("/jobs/{job_id}/status")
def job_status(job_id: str):
    return get_job_status(job_id)


@app.post("/separate")
def separate_song(song: UploadFile):
    upload_file_obj(song.file, song.filename)

    # job = separate_song_parts.queue(path)
    # status = job.get_status()

    # return '<a href="/api/jobs/' + job.id + '/status">' + status + "</a>"
