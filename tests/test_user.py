from fastapi.testclient import TestClient

from src.main import app

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
    response = client.get("/api/v1/user", params={'email': "not.exists@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        "name": "Test User",
        "email": "test.user@mail.com"
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)
    
    response_get = client.get("/api/v1/user", params={"email": new_user["email"]})
    assert response_get.status_code == 200
    assert response_get.json()["name"] == new_user["name"]
    assert response_get.json()["email"] == new_user["email"]

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email = users[0]['email']
    new_user = {
        "name": "Duplicate User",
        "email": existing_email
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    temp_user = {
        "name": "Temp User",
        "email": "temp.user@mail.com"
    }
    client.post("/api/v1/user", json=temp_user)

    response_delete = client.delete("/api/v1/user", params={"email": temp_user["email"]})
    assert response_delete.status_code == 204
    
    response_get = client.get("/api/v1/user", params={"email": temp_user["email"]})
    assert response_get.status_code == 404