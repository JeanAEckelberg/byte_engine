from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app
import pytest

client = TestClient(app=app)


# Test leaderboard method in main.py

# Test get method


def test_get_leaderboard():
    response = client.get('/leaderboard/')

    assert response.status_code == 200
    assert response.json() == [
        {"group_run_id": 1, "start_run": "2000-10-31T06:30:00Z", "launcher_version": "12", "runs_per_client": 1,
         "is_finished": True, "runs": [
            {"run_id": 1, "group_run_id": 1, "run_time": "2000-10-31T06:30:00Z", "seed": 1, "results": "test",
             "submission_run_infos": [
                 {"submission_run_info_id": 1, "run_id": 1, "submission_id": 1, "error_txt": "error", "player_num": 1,
                  "points_awarded": 100,
                  "submission": {"submission_id": 1, "submission_time": "2000-10-31T06:30:00Z", "file_txt": "test"}}],
             "turn_tables": [{"turn_id": 1, "turn_number": 1, "run_id": 1, "turn_data": "test"}]}], "group_teams": [
            {"group_teams_id": 1, "group_run_id": 1, "team_uuid": "1",
             "team": {"uni_id": 1, "team_type_id": 1, "team_name": "Noobs",
                      "university": {"uni_id": 1, "uni_name": "NDSU"},
                      "team_type": {"team_type_id": 1, "team_type_name": "Undergrad", "eligible": True},
                      "submissions": [
                          {"submission_id": 1, "submission_time": "2000-10-31T06:30:00Z", "file_txt": "test",
                           "submission_run_infos": [
                               {"submission_run_info_id": 1, "run_id": 1, "submission_id": 1, "error_txt": "error",
                                "player_num": 1, "points_awarded": 100,
                                "run": {"run_id": 1, "group_run_id": 1, "run_time": "2000-10-31T06:30:00Z", "seed": 1,
                                        "results": "test"}}]}]}}]},
        {"group_run_id": 2, "start_run": "2000-10-31T06:30:00Z", "launcher_version": "10", "runs_per_client": 2,
         "is_finished": False, "runs": [], "group_teams": [{"group_teams_id": 2, "group_run_id": 2, "team_uuid": "1",
                                                            "team": {"uni_id": 1, "team_type_id": 1,
                                                                     "team_name": "Noobs",
                                                                     "university": {"uni_id": 1, "uni_name": "NDSU"},
                                                                     "team_type": {"team_type_id": 1,
                                                                                   "team_type_name": "Undergrad",
                                                                                   "eligible": True}, "submissions": [
                                                                    {"submission_id": 1,
                                                                     "submission_time": "2000-10-31T06:30:00Z",
                                                                     "file_txt": "test", "submission_run_infos": [
                                                                        {"submission_run_info_id": 1, "run_id": 1,
                                                                         "submission_id": 1, "error_txt": "error",
                                                                         "player_num": 1, "points_awarded": 100,
                                                                         "run": {"run_id": 1, "group_run_id": 1,
                                                                                 "run_time": "2000-10-31T06:30:00Z",
                                                                                 "seed": 1, "results": "test"}}]}]}}]}]
