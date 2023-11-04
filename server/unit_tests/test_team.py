from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app=app)

# Test Team methods in main.py

# Test post method


def test_team_post():
    response = client.post('/team/',
                           json={"uni_id": 1,
                                 "team_type_id": 1,
                                 "team_name": "Noobss"}
                           )
    assert response.status_code == 200
    assert response.json()['uni_id'] == 1
    assert response.json()['team_type_id'] == 1
    assert response.json()['team_name'] == "Noobss"
