from os import environ
from urllib.parse import urlparse

from redis import Redis
from rq import Queue

if environ.get("REDISCLOUD_URL") is None:
    r = Redis()
else:
    url = urlparse(environ.get("REDISCLOUD_URL"))
    r = Redis(host=url.hostname, port=url.port, password=url.password)
q = Queue(connection=r)


def enqueue_job(func, *args):
    """
    Enqueue a job to be processed by a worker
    :param func: Function to be executed
    :param args: Arguments to be passed to the function
    :return: Job ID
    """

    result = q.enqueue(func, *args)
    return result.get_id()


def get_job_status(job_id):
    """
    Get the status of a job
    :param job_id: Job ID
    :return: Job status
    """

    job = q.fetch_job(job_id)
    if job is None:
        return "Job not found"
    return job.get_status()


def get_job_by_id(job_id):
    """
    Get a job by id
    :param job_id: Job ID
    :return: Job object
    """

    job = q.fetch_job(job_id)
    if job is None:
        return "Job not found"
    return job
