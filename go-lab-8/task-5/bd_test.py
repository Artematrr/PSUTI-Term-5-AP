# import unittest
# import threading
# import requests
# import json
# from time import sleep
# from bd import run


# class TestUserAPI(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Запускаем сервер на отдельном потоке
#         cls.server_thread = threading.Thread(target=run)
#         cls.server_thread.daemon = True
#         cls.server_thread.start()
#         sleep(1)  # Даем серверу время на запуск

#         cls.base_url = "http://localhost:8080/users"

#     def test_1_post_user(self):
#         """Тестирование создания нового пользователя (POST /users)"""
#         new_user = {"name": "John Doe", "age": 30}
#         response = requests.post(self.base_url, json=new_user)
#         self.assertEqual(response.status_code, 201)
#         user = response.json()
#         self.assertEqual(user["name"], "John Doe")
#         self.assertEqual(user["age"], 30)
#         # Сохраняем ID для последующих тестов
#         self.__class__.created_user_id = user["id"]

#     def test_2_get_users(self):
#         """Тестирование получения списка пользователей (GET /users)"""
#         response = requests.get(self.base_url)
#         self.assertEqual(response.status_code, 200)
#         users = response.json()
#         self.assertGreater(len(users), 0)  # Проверяем, что пользователи есть

#     def test_3_get_user_by_id(self):
#         """Тестирование получения пользователя по ID (GET /users/{id})"""
#         user_id = self.__class__.created_user_id
#         response = requests.get(f"{self.base_url}/{user_id}")
#         self.assertEqual(response.status_code, 200)
#         user = response.json()
#         self.assertEqual(user["id"], user_id)

#     def test_4_put_user(self):
#         """Тестирование обновления данных пользователя (PUT /users/{id})"""
#         user_id = self.__class__.created_user_id
#         updated_user = {"name": "John Updated", "age": 35}
#         response = requests.put(
#             f"{self.base_url}/{user_id}", json=updated_user)
#         self.assertEqual(response.status_code, 200)
#         user = response.json()
#         self.assertEqual(user["name"], "John Updated")
#         self.assertEqual(user["age"], 35)

#     def test_5_delete_user(self):
#         """Тестирование удаления пользователя (DELETE /users/{id})"""
#         user_id = self.__class__.created_user_id
#         response = requests.delete(f"{self.base_url}/{user_id}")
#         # Успешное удаление не возвращает данных
#         self.assertEqual(response.status_code, 204)

#         # Проверяем, что пользователь действительно удалён
#         response = requests.get(f"{self.base_url}/{user_id}")
#         self.assertEqual(response.status_code, 404)

#     def test_6_pagination(self):
#         """Тестирование пагинации (GET /users?limit=2&offset=0)"""
#         response = requests.get(f"{self.base_url}?limit=2&offset=0")
#         self.assertEqual(response.status_code, 200)
#         users = response.json()
#         # Проверяем, что возвращено не больше 2 пользователей
#         self.assertLessEqual(len(users), 2)

#     def test_7_filter_by_name(self):
#         """Тестирование фильтрации по имени (GET /users?name=John)"""
#         response = requests.get(f"{self.base_url}?name=John")
#         self.assertEqual(response.status_code, 200)
#         users = response.json()
#         for user in users:
#             self.assertIn("John", user["name"])

#     @classmethod
#     def tearDownClass(cls):
#         # Сервер автоматически завершится при завершении тестов
#         pass


# if __name__ == '__main__':
#     unittest.main()
import unittest
import requests
import json

BASE_URL = "http://localhost:8080/users"

class TestUserAPI(unittest.TestCase):

    def test_get_all_users(self):
        print("\nTesting GET /users")
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print("Тест GET /users успешно пройден")

    def test_get_single_user(self):
        print("\nTesting GET /users/<id> ")
        response = requests.get(f"{BASE_URL}/1")  # Пример с ID = 1
        if response.status_code == 200:
            data = response.json()
            self.assertEqual(data["id"], 1)
            print("Пользователь с ID 1 найден")
        else:
            self.assertEqual(response.status_code, 404)
            print("Пользователь с ID 1 не найден")
        print("Тест GET /users/<id> успешно пройден")

    def test_create_user(self):
        print("\nTesting POST /users ")
        new_user = {"name": "Alice", "age": 30}
        response = requests.post(BASE_URL, json=new_user)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], new_user["name"])
        self.assertEqual(data["age"], new_user["age"])
        self.assertIn("id", data)
        print(f"Пользователь {data} успешно создан")
        print("Тест POST /users успешно пройден")

    def test_update_user(self):
        print("\nTesting PUT /users/<id>")
        updated_user = {"name": "Bob", "age": 35}
        response = requests.put(f"{BASE_URL}/1", json=updated_user)  # Пример с ID = 1
        if response.status_code == 200:
            data = response.json()
            self.assertEqual(data["name"], updated_user["name"])
            self.assertEqual(data["age"], updated_user["age"])
            print(f"Пользователь {data} успешно обновлен")
        else:
            self.assertEqual(response.status_code, 404)
            print("Пользователь с ID 1 не найден для обновления")
        print("Тест PUT /users/<id> успешно пройден")

    def test_delete_user(self):
        print("\nTesting DELETE /users/<id>")
        response = requests.delete(f"{BASE_URL}/1")  # Пример с ID = 1
        if response.status_code == 204:
            print("Пользователь с ID 1 успешно удален")
            self.assertEqual(response.status_code, 204)
        else:
            self.assertEqual(response.status_code, 404)
            print("Пользователь с ID 1 не найден для удаления")
        print("Тест DELETE /users/<id> успешно пройден")


if __name__ == "__main__":
    unittest.main(verbosity=2)
