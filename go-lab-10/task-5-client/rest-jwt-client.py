import requests
import json

base_url = "http://localhost:8080"


def login(username):
    try:
        response = requests.post(f"{base_url}/login", json={"name": username})
        response.raise_for_status()
        token = response.json().get("token")
        print("\nТокен аутентификации:", token)
        return token
    except requests.exceptions.HTTPError as err:
        print("Ошибка авторизации:", response.status_code, response.text)
        return None
    except Exception as e:
        print("Произошла ошибка при авторизации:", e)
        return None


def get_users(token):
    headers = {"Authorization": token}
    try:
        response = requests.get(f"{base_url}/users", headers=headers)
        response.raise_for_status()
        print("Список пользователей:", response.json())
    except requests.exceptions.HTTPError as err:
        print("Ошибка при получении списка пользователей:",
              response.status_code, response.text)
    except Exception as e:
        print("Произошла ошибка при получении пользователей:", e)


def create_user(token, name, age, role):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    user_data = {"name": name, "age": age, "role": role}
    try:
        response = requests.post(
            f"{base_url}/users", headers=headers, json=user_data)
        response.raise_for_status()  # Проверка на успешный статус ответа
        print("Пользователь добавлен:", response.json())
    except requests.exceptions.HTTPError as err:
        print("Ошибка при добавлении пользователя:",
              response.status_code, response.text)
    except Exception as e:
        # print("Произошла ошибка при добавлении пользователя:", e)
        print("Недостаточно прав!",)


if __name__ == "__main__":
    # token = login("Admin")
    token = login("Андрейка")
    if token:
        print()
        get_users(token)
        print()
        create_user(token, "Типчикус", 22, "user")
        print()
        get_users(token)
