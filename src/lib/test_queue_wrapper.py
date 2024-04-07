import unittest
from unittest.mock import patch

import fakeredis

from .queue_wrapper import enqueue_job, get_job_by_id, get_job_status


class TestQueueWrapper(unittest.TestCase):
    @patch("redis_instance", fakeredis.FakeStrictRedis())
    def test_enqueue_job(self):
        # Test case 1: Enqueue a job with a function and arguments
        def add(a, b):
            return a + b

        job_id = enqueue_job(add, 2, 3)
        self.assertIsNotNone(job_id)
        # Add assertions to check if the job is enqueued correctly

        # Test case 2: Enqueue a job with a function and no arguments
        def greet():
            return "Hello, world!"

        job_id = enqueue_job(greet)
        self.assertIsNotNone(job_id)
        # Add assertions to check if the job is enqueued correctly

        # Test case 3: Enqueue a job with a function and multiple arguments
        def multiply(a, b, c):
            return a * b * c

        job_id = enqueue_job(multiply, 2, 3, 4)
        self.assertIsNotNone(job_id)
        # Add assertions to check if the job is enqueued correctly

    @patch("redis_instance", fakeredis.FakeStrictRedis())
    def test_get_job_status(self):
        # Test case 1: Get status of an existing job
        job_id = enqueue_job(lambda: None)
        status = get_job_status(job_id)
        self.assertIsNotNone(status)
        # Add assertions to check if the status is correct

        # Test case 2: Get status of a non-existing job
        job_id = "non_existing_job_id"
        status = get_job_status(job_id)
        self.assertEqual(status, "Job not found")
        # Add assertions to check if the status is correct

    @patch("redis_instance", fakeredis.FakeStrictRedis())
    def test_get_job_by_id(self):
        # Test case 1: Get an existing job by id
        job_id = enqueue_job(lambda: None)
        job = get_job_by_id(job_id)
        self.assertIsNotNone(job)
        # Add assertions to check if the job is retrieved correctly

        # Test case 2: Get a non-existing job by id
        job_id = "non_existing_job_id"
        job = get_job_by_id(job_id)
        self.assertIsNone(job)
        # Add assertions to check if the job is retrieved correctly


if __name__ == "__main__":
    unittest.main()
