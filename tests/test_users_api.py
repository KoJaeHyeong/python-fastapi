

from database.orm import User
from database.repository import UserRepository
from service.user import UserService


def test_sign_up(client, mocker):

    hash_password = mocker.patch.object(UserService, "hash_password", return_value="hashed")

    create_user = mocker.patch.object(User, "create", return_value= User(id=None, username="test_user", password="hashed"))

    mocker.patch.object(UserRepository, "create_user", return_value=User(id=1, username="test_user", password="hashed"))

    body = {
        "username": "test_user",
        "password": "test_password"
    }

    response = client.post("/user/sign-up", json=body)

    hash_password.assert_called_once_with(password="test_password")
    create_user.assert_called_once_with(username="test_user", hashed_password="hashed")


    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "test_user"}
