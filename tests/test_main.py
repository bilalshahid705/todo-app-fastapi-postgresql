from fastapi.testclient import TestClient
from fastapi import status
import pytest

from sqlmodel import SQLModel, create_engine, Session
from app.settings import settings
from app.main import app
from app.database import get_session

test_database_url = str(settings.TEST_DATABASE_URL).replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(test_database_url, echo=True)


@pytest.fixture(scope="module", autouse=True)
def get_db_session():
    SQLModel.metadata.create_all(engine)
    yield Session(engine)

@pytest.fixture(scope="function")
def test_app(get_db_session):
    def test_session():
        yield get_db_session

    app.dependency_overrides[get_session] = test_session

    with TestClient(app=app) as client:
        yield client

    app.dependency_overrides.clear()

def test_root():
    client = TestClient(app=app)
    response = client.get("/")
    data = response.json()
    assert data == {
        "message": "Welcome to dailyDo todo app",
        "data": None,
        "status": status.HTTP_200_OK,
    }


def test_create_todo(test_app):
    test_todo = {"content":"creating test case", "is_completed":False}
    response = test_app.post('/todos/',json=test_todo)
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert data["data"]["content"] == test_todo["content"]

def test_get_single_todo(test_app):
    test_todo = {"content":"get single todo test", "is_completed":False}
    response = test_app.post('/todos/',json=test_todo)
    todo_id = response.json()["data"]["id"]

    res = test_app.get(f'/todos/{todo_id}')
    data = res.json()
    assert res.status_code == 200
    assert data["data"]["content"] == test_todo["content"]


def test_edit_todo(test_app):
    test_todo = {"content":"edit todo test", "is_completed":False}
    response = test_app.post('/todos/',json=test_todo)
    todo_id = response.json()["data"]["id"]

    edited_todo = {"content":"We have edited this", "is_completed":False}
    response = test_app.put(f'/todos/{todo_id}',json=edited_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["data"]["content"] == edited_todo["content"]


def test_delete_todo(test_app):
    test_todo = {"content":"delete todo test", "is_completed":False}
    response = test_app.post('/todos/',json=test_todo)
    todo_id = response.json()["data"]["id"]

    response = test_app.delete(f'/todos/{todo_id}')
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Todo deleted successfully"