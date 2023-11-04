from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test Run methods in main.py

# Test get_run method
def test_get_run():
    # NEEDS IMPLEMENTATION
    ...


# Test run method
def test_run():
    response = client.get('/run/')

    assert response.status_code == 200
    assert response.json() == [{"run_id": 1,
                                "group_run_id": 1,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 1,
                                "results": "test"},
                               {"run_id": 2,
                                "group_run_id": 1,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 2,
                                "results": "test"},
                               {"run_id": 3,
                                "group_run_id": 2,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 1,
                                "results": "test"},
                               {"run_id": 4,
                                "group_run_id": 2,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 2,
                                "results": "test"}
                               ]
