from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test Submission methods in main.py

# Test post method


def test_post_submission():
    response = client.post('/submission/',
                           json={"team_uuid": '1',
                                 "submission_id": 2,
                                 "submission_time": "2000-10-31T01:30:00-05:00",
                                 "file_txt": 'test'}
                           )
    assert response.status_code == 200
    assert response.json() == {"submission_id": 2,
                               "submission_time": "2000-10-31T06:30:00Z",
                               "file_txt": "test"}


# Test get methods

def test_get_submission():
    response = client.get('/get_submission/1/1/')
    assert response.status_code == 200
    assert response.json() == {"submission_id": 1,
                               "submission_time": "2000-10-31T06:30:00Z",
                               "file_txt": "test",
                               "team": {"uni_id": 1,
                                        "team_type_id": 1,
                                        "team_name": "Noobs"},
                               "submission_run_infos": [{"submission_run_info_id": 1,
                                                         "run_id": 1,
                                                         "submission_id": 1,
                                                         "error_txt": "error",
                                                         "player_num": 1,
                                                         "points_awarded": 100,
                                                         "run": {"run_id": 1,
                                                                 "group_run_id": 1,
                                                                 "run_time": "2000-10-31T06:30:00Z",
                                                                 "seed": 1,
                                                                 "results": "test"}}]}


def test_get_submissions():
    response = client.get('/get_submissions/1')
    assert response.status_code == 200
    assert response.json() == [{"submission_id": 1, "submission_time": "2000-10-31T06:30:00Z", "file_txt": "test",
                                "team": {"uni_id": 1, "team_type_id": 1, "team_name": "Noobs"},
                                "submission_run_infos": [
                                    {"submission_run_info_id": 1, "run_id": 1, "submission_id": 1, "error_txt": "error",
                                     "player_num": 1, "points_awarded": 100,
                                     "run": {"run_id": 1, "group_run_id": 1, "run_time": "2000-10-31T06:30:00Z",
                                             "seed": 1, "results": "test"}}]},
                               {"submission_id": 2, "submission_time": "2000-10-31T06:30:00Z", "file_txt": "test",
                                "team": {"uni_id": 1, "team_type_id": 1, "team_name": "Noobs"},
                                "submission_run_infos": []}]


# Test read nonexistent submission/s


def test_get_nonexistent_submission():
    with pytest.raises(IndexError):
        client.get('/get_submission/3/2')
