import asyncio
import os
from typing import Union

import redis
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel
from rq import Queue

from .module_example import count_string_len

load_dotenv()

app = FastAPI()
r = redis.from_url(os.getenv("REDIS_URL"))
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


@app.get("/string_len/{string}")
def string_len(string: str):
    job = q.enqueue(count_string_len, string)
    job_id = job.get_id()
    return RedirectResponse(f"/jobs/{job_id}/status")


@app.get("/jobs/{job_id}/status")
def job_status(job_id: str):
    return StreamingResponse(get_job_status(job_id))


async def get_job_status(job_id: str):
    job = q.fetch_job(job_id)
    if job is None:
        yield "not_found"
        return
    while job.get_status() != "finished":
        await asyncio.sleep(0.1)
        yield job.get_status()
