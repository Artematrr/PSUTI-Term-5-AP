import json
import requests

session_token = ""
is_authorized = False


def login(username, password):
    global session_token, is_authorized
    response = requests.post(
        'http://localhost:8080/login', json={"name": username, "password": password})

    if response.status_code == 200:
        session_token = response.headers.get('Authorization')
        is_authorized = True
        print("Авторизация успешна")
    else:
        print("Ошибка авторизации:", response.json().get("error"))
        session_token = ""
        is_authorized = False


def authorized_request(method, url, data=None):
    headers = {
        'Authorization': session_token,
        'Content-Type': 'application/json'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)

    return response


def get_users():
    response = authorized_request('GET', 'http://localhost:8080/users')
    if response.status_code == 200:
        users = response.json()
        print("Пользователи:")
        for user in users:
            print(f"ID: {user['id']}, Имя: {
                  user['name']}, Возраст: {user['age']}")
    else:
        print("Ошибка:", response.json().get("error"))


def get_user_by_id(user_id):
    response = authorized_request(
        'GET', f'http://localhost:8080/users/{user_id}')
    if response.status_code == 200:
        user = response.json()
        print(f"Пользователь: ID: {user['id']}, Имя: {
              user['name']}, Возраст: {user['age']}")
    else:
        print("Ошибка:", response.json().get("error"))


def create_user(name, age, password):
    user = {'name': name, 'age': age, 'password': password}
    response = authorized_request('POST', 'http://localhost:8080/users', user)
    if response.status_code == 201:
        print("Пользователь успешно создан")
    else:
        print("Ошибка:", response.json().get("error"))


def update_user(user_id, name, age, password):
    user = {'name': name, 'age': age, 'password': password}
    response = authorized_request(
        'PUT', f'http://localhost:8080/users/{user_id}', user)
    if response.status_code == 200:
        print("Пользователь успешно обновлен")
    else:
        print("Ошибка:", response.json().get("error"))


def delete_user(user_id):
    response = authorized_request(
        'DELETE', f'http://localhost:8080/users/{user_id}')
    if response.status_code == 200:
        print("Пользователь успешно удален")
    else:
        print("Ошибка:", response.json().get("error"))


def main():
    global session_token, is_authorized

    while True:
        if not is_authorized:
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            login(username, password)

        if is_authorized:
            print("\nВыберите:")
            print("\t1. Получить всех пользователей")
            print("\t2. Получить пользователя по ID")
            print("\t3. Создать пользователя")
            print("\t4. Обновить пользователя")
            print("\t5. Удалить пользователя")
            print("\t6. Выйти")
            choice = input("Действие: ")

            if choice == '1':
                get_users()
            elif choice == '2':
                user_id = input("Введите ID пользователя: ")
                get_user_by_id(user_id)
            elif choice == '3':
                name = input("Имя пользователя: ")
                age = input("Возраст пользователя: ")
                password = input("Пароль пользователя: ")
                create_user(name, age, password)
            elif choice == '4':
                user_id = input("Введите ID пользователя: ")
                name = input("Имя пользователя: ")
                age = input("Возраст пользователя: ")
                password = input("Пароль пользователя: ")
                update_user(user_id, name, age, password)
            elif choice == '5':
                user_id = input("Введите ID пользователя: ")
                delete_user(user_id)
            elif choice == '6':
                print("Выход...")
                break
            else:
                print("Некорректный выбор.")


if __name__ == "__main__":
    main()
