from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test Submission methods in main.py

# Test get method

def test_get_group_runs():
    response = client.get('/group_runs/')

    assert response.status_code == 200
    assert response.json() == [{"group_run_id": 1,
                                     "start_run": "2000-10-31T06:30:00Z",
                                     "launcher_version": "12",
                                     "runs_per_client": 1,
                                     "is_finished": True},
                                    {"group_run_id": 2,
                                     "start_run": "2000-10-31T06:30:00Z",
                                     "launcher_version": "10",
                                     "runs_per_client": 2,
                                     "is_finished": False}]
