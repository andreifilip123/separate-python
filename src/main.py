from cuid import cuid
from fastapi import FastAPI
from pydantic import BaseModel

from .lib.queue_wrapper import enqueue_job, get_job_by_id, get_job_status
from .lib.separate_wrapper import separate_song_parts

app = FastAPI()


@app.get("/jobs/{job_id}/status")
def job_status(job_id: str):
    job = get_job_by_id(job_id)
    response = {"status": get_job_status(job_id), "result": None}
    if job is None:
        return response
    result = job.latest_result()
    if result is None or result.return_value is None:
        return response
    no_vocals = result.return_value["no_vocals"]
    vocals = result.return_value["vocals"]

    response["result"] = {"no_vocals": no_vocals, "vocals": vocals}

    return response


class SeparateRequestParams(BaseModel):
    song_url: str


@app.post("/separate")
def separate_song(params: SeparateRequestParams):
    unique_id = cuid()
    print("Separating song parts", unique_id)
    try:
        job_id = enqueue_job(separate_song_parts, params.song_url, unique_id)
        print("Enqueued job", job_id)
        # 4. Return the job ID
        return {"job_id": job_id, "status": get_job_status(job_id)}
    except Exception as e:
        print("Error", e)
        return {"error": str(e)}
