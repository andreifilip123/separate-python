from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def fake_test():
    assert "true" == "true"
