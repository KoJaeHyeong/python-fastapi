import pytest
from fastapi.testclient import TestClient
from main import app


# client를 재사용하기 위함.(pytest fixture 역할)
@pytest.fixture
def client():
    return TestClient(app=app)
