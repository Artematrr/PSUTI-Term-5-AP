import json
import requests


class User:
    def __init__(self, user_id, name, age):
        self.id = user_id
        self.name = name
        self.age = age


def get_users():
    response = requests.get("http://localhost:8080/users")
    if response.status_code == 200:
        users = response.json()
        print("Список пользователей:")
        for user in users:
            print(f"ID: {user['id']}, Имя: {
                  user['name']}, Возраст: {user['age']}")
    else:
        print("Ошибка при получении списка пользователей:", response.text)


def get_user_by_id(user_id):
    response = requests.get(f"http://localhost:8080/users/{user_id}")
    if response.status_code == 200:
        user = response.json()
        print(
            f"Вывод пользователя - ID: {user['id']}, Имя: {user['name']}, Возраст: {user['age']}")
    else:
        print("Ошибка при получении пользователя:", response.text)


def create_user(name, age):
    user = User(None, name, age)
    response = requests.post("http://localhost:8080/users", json=user.__dict__)
    if response.status_code == 201:
        created_user = response.json()
        print(f"Пользователь создан с ID: {created_user['id']}")
    else:
        print("Ошибка при создании пользователя:", response.text)


def create_user_with_id(user_id, name, age):
    user = User(user_id, name, age)
    response = requests.post(
        f"http://localhost:8080/users/{user_id}", json=user.__dict__)
    if response.status_code == 201:
        created_user = response.json()
        print(f"Пользователь создан с ID: {created_user['id']}")
    else:
        print("Ошибка при создании пользователя:", response.text)


def update_user(user_id, name, age):
    user = User(user_id, name, age)
    response = requests.put(
        f"http://localhost:8080/users/{user_id}", json=user.__dict__)
    if response.status_code == 200:
        print("Пользователь обновлен успешно.")
    else:
        print("Ошибка при обновлении пользователя:", response.text)


def delete_user(user_id):
    response = requests.delete(f"http://localhost:8080/users/{user_id}")
    if response.status_code == 204:
        print("Пользователь удален успешно.")
    else:
        print("Ошибка при удалении пользователя:", response.text)


def main():
    while True:
        print("\nВыберите:")
        print("\t1. Получить список пользователей")
        print("\t2. Получить пользователя по ID")
        print("\t3. Создать пользователя")
        print("\t4. Создать пользователя по ID")
        print("\t5. Обновить пользователя")
        print("\t6. Удалить пользователя")
        print("\t0. Выход")

        choice = input("Действие: ")

        if choice == "1":
            get_users()
        elif choice == "2":
            user_id = int(input("Введите ID пользователя: "))
            get_user_by_id(user_id)
        elif choice == "3":
            name = input("Введите имя пользователя: ")
            age = int(input("Введите возраст пользователя: "))
            create_user(name, age)
        elif choice == "4":
            user_id = int(input("Введите ID пользователя: "))
            name = input("Введите имя пользователя: ")
            age = int(input("Введите возраст пользователя: "))
            create_user_with_id(user_id, name, age)
        elif choice == "5":
            user_id = int(input("Введите ID пользователя: "))
            name = input("Введите новое имя пользователя: ")
            age = int(input("Введите новый возраст пользователя: "))
            update_user(user_id, name, age)
        elif choice == "6":
            user_id = int(input("Введите ID пользователя: "))
            delete_user(user_id)
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
