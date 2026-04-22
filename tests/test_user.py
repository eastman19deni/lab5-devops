from fastapi.testclient import TestClient
from src.main import app
from src.schemas.user import CreateUser

client = TestClient(app)

# Существующие пользователи (должны совпадать с данными в API)
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',  # ✅ Исправлено под реальный ответ API
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'VOva KApral',
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
    response = client.get("/api/v1/user", params={'email': "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    test_data = CreateUser(  # ✅ Исправлено: было Creator
        name="Test User",
        email="test_create@mail.com",
    ).model_dump()
    response = client.post("/api/v1/user", json=test_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test_create@mail.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    test_data = CreateUser(
        name="Duplicate User",
        email="i.i.ivanov@mail.com",
    ).model_dump()
    response = client.post("/api/v1/user", json=test_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"


def test_delete_user():
    '''Удаление пользователя'''
    # Создаем пользователя для удаления
    create_data = CreateUser(
        name="To Be Deleted",
        email="to_delete@mail.com",
    ).model_dump()
    create_response = client.post("/api/v1/user", json=create_data)
    assert create_response.status_code == 201
    
    # Удаляем его
    response = client.delete("/api/v1/user", params={'email': "to_delete@mail.com"})
    assert response.status_code == 204
    
    # Проверяем, что действительно удален
    get_response = client.get("/api/v1/user", params={'email': "to_delete@mail.com"})
    assert get_response.status_code == 404