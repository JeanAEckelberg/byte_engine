from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app=app)


def test_read_root():
    response = client.get('/')
    assert response.json() == {'message': 'Hello World'}


def test_read_get_submission():
    response = client.get('/get_submission/1/1/')
    print(response.json())
    assert response.json() == {
        'submission_id': 1,
        'submission_time': '2000-10-31T01:30:00.000-05:00',
        'file_txt': 'test',
        'team_uuid': 1,
    }
