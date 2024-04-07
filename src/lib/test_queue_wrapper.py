import unittest
from unittest.mock import patch

from fakeredis import FakeRedis

from .queue_wrapper import enqueue_job, get_job_by_id, get_job_status


class TestQueueWrapper(unittest.TestCase):
    def test_enqueue_job(self):
        with patch("src.lib.queue_wrapper.Redis", FakeRedis):
            # Test case 1: Enqueue a job with a function and arguments
            def add(a, b):
                return a + b

            job_id = enqueue_job(add, 2, 3)
            self.assertIsNotNone(job_id)

            # Test case 2: Enqueue a job with a function and no arguments
            def greet():
                return "Hello, world!"

            job_id = enqueue_job(greet)
            self.assertIsNotNone(job_id)

            # Test case 3: Enqueue a job with a function and multiple arguments
            def multiply(a, b, c):
                return a * b * c

            job_id = enqueue_job(multiply, 2, 3, 4)
            self.assertIsNotNone(job_id)

    def test_get_job_status(self):
        with patch("src.lib.queue_wrapper.Redis", FakeRedis):
            # Test case 1: Get status of an existing job
            job_id = enqueue_job(lambda: None)
            status = get_job_status(job_id)
            self.assertIsNotNone(status)

            # Test case 2: Get status of a non-existing job
            job_id = "non_existing_job_id"
            status = get_job_status(job_id)
            self.assertEqual(status, "Job not found")

    def test_get_job_by_id(self):
        with patch("src.lib.queue_wrapper.Redis", FakeRedis):
            # Test case 1: Get an existing job by id
            job_id = enqueue_job(lambda: None)
            job = get_job_by_id(job_id)
            self.assertIsNotNone(job)

            # Test case 2: Get a non-existing job by id
            job_id = "non_existing_job_id"
            job = get_job_by_id(job_id)
            self.assertIsNone(job)


if __name__ == "__main__":
    unittest.main()
