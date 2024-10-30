import json
import requests

BASE_URL = "http://localhost:8080"

class User:
    def __init__(self, id, name, age, role):
        self.id = id
        self.name = name
        self.age = age
        self.role = role

def login(name):
    login_url = f"{BASE_URL}/login"
    response = requests.post(login_url, json={"name": name})

    if response.status_code == 200:
        data = response.json()
        print("Вход выполнен. Токен:", data["token"], "CSRF-токен:", data["csrf_token"])
        return data["token"], data["csrf_token"]
    else:
        print("Не удалось войти. Статус код:", response.status_code)
        return None, None

def get_users(token, csrf_token):
    user_url = f"{BASE_URL}/users"
    headers = {
        "Authorization": token,
        "X-CSRF-Token": csrf_token
    }
    response = requests.get(user_url, headers=headers)

    if response.status_code == 200:
        users = [User(**user) for user in response.json()]
        print("Список пользователей:")
        for user in users:
            print(f"ID: {user.id}, Имя: {user.name}, Возраст: {user.age}, Роль: {user.role}")
    else:
        print("Не удалось получить пользователей. Статус код:", response.status_code)

def create_user(token, csrf_token, name, age, role):
    user_url = f"{BASE_URL}/users"
    headers = {
        "Authorization": token,
        "X-CSRF-Token": csrf_token,
        "Content-Type": "application/json"
    }
    new_user = {
        "name": name,
        "age": age,
        "role": role
    }
    response = requests.post(user_url, json=new_user, headers=headers)

    if response.status_code == 200:
        user = User(**response.json())
        print("Пользователь создан:", user.__dict__)
    else:
        print("Не удалось создать пользователя. Статус код:", response.status_code)

def main():
    # token, csrf_token = login("Андрейка")
    token, csrf_token = login("Admin")
    if token and csrf_token:
        get_users(token, csrf_token)
        create_user(token, csrf_token, "Щеколда", 25, "user")
        get_users(token, csrf_token)

if __name__ == "__main__":
    main()