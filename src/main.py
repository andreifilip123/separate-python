from cuid import cuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .lib.queue_wrapper import enqueue_job, get_job_by_id, get_job_status
from .lib.separate_wrapper import separate_song_parts

origins = ["http://localhost:3000"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/jobs/{job_id}/status")
def job_status(job_id: str):
    job = get_job_by_id(job_id)
    if job is None:
        return {"status": "Job not found", "result": None}
    result = job.latest_result()
    if (
        result is not None
        and result.type == result.Type.SUCCESSFUL
        and result.return_value is not None
    ):
        no_vocals = result.return_value["no_vocals"]
        vocals = result.return_value["vocals"]

        return {
            "status": get_job_status(job_id),
            "result": {"no_vocals": no_vocals, "vocals": vocals},
        }
    else:
        return {"status": get_job_status(job_id), "result": None}


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
