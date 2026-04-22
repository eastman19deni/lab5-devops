from fastapi.testclient import TestClient

from src.main import app

from src.schemas.user import CreateUser

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': "test@mail.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    test_data = CreateUser(
        name="Test User",
        email="test@mail.com",
    ).model_dump()
    response = client.post("/api/v1/user", json=test_data)
    assert response.status_code == 201
    assert response.json() is not None


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    test_data = CreateUser(
        name="Test User",
        email="i.i.ivanov@mail.com",
    ).model_dump()
    response = client.post("/api/v1/user", json=test_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"


def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete("/api/v1/user", params={'email': "test@mail.com"})
    assert response.status_code == 204
