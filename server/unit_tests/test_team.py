from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app=app)

# Test Team methods in main.py

# Test post method


