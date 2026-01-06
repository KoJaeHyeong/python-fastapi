from api.todo import User, UserRepository, UserService
from database.orm import Todo
from database.repository import TodoRepository

# client = TestClient(app=app)  # test 클라이언트를 생성 (실제 클라이언트와 비슷한 역할)

def test_get_todos(client, mocker):
    access_token: str = UserService().create_jwt(username="test")
    headers = { "Authorization": f"Bearer {access_token}" }

    user = User(id=1, username="test", password="hashed")
    user.todos = [Todo(id=1, contents="첫번째", is_done=True), Todo(id=2, contents="두번째", is_done=False)]

    mocker.patch.object(UserRepository, "get_user_by_username", return_value=user)
    print(headers)
    response = client.get("/todos", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "첫번째", "is_done": True},
            {"id": 2, "contents": "두번째", "is_done": False},
            # {"id": 3, "contents": "세번째", "is_done": False},
            # {"id": 5, "contents": "다섯번째", "is_done": False},
            # {"id": 6, "contents": "여섯번째", "is_done": False},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            # {"id": 6, "contents": "여섯번째", "is_done": False},
            # {"id": 5, "contents": "다섯번째", "is_done": False},
            # {"id": 3, "contents": "세번째", "is_done": False},
            {"id": 2, "contents": "두번째", "is_done": False},
            {"id": 1, "contents": "첫번째", "is_done": True},
        ]
    }


def test_get_todo(client, mocker):
    # 200
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_id",
        return_value=Todo(id=1, contents="첫번째", is_done=True),
    )

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "첫번째", "is_done": True}

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_id", return_value=None)

    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(client, mocker):
    create_spy = mocker.spy(Todo, "create")
    mocker.patch.object(
        TodoRepository,
        "create_new_todo",
        return_value=Todo(id=1, contents="todo", is_done=True),
    )

    body = {
        "contents": "test",
        "is_done": False,
    }
    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None  # create로 return된 값이 할당
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}


def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_id",
        return_value=Todo(id=1, contents="첫번째", is_done=True),
    )

    undone = mocker.patch.object(Todo, "undone")

    mocker.patch.object(
        TodoRepository,
        "update_todo_done",
        return_value=Todo(id=1, contents="첫번째", is_done=False),
    )

    response = client.patch("/todos/1", json={"is_done": False})

    undone.assert_called_once_with()  # undone 메서드가 1번 호출되었는지 확인. body값에 따라 확인

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "첫번째", "is_done": False}

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_id", return_value=None)

    response = client.patch("/todos/1", json={"is_done": True})

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(client, mocker):
    # 204
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_id",
        return_value=Todo(id=1, contents="todo", is_done=True),
    )
    mocker.patch.object(TodoRepository, "delete_todo_by_id", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_id", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
