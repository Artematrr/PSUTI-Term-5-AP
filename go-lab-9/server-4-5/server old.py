#  1
# # import json
# # import random
# # import string
# # from http.server import BaseHTTPRequestHandler, HTTPServer
# # import psycopg2

# # # Настройка базы данных
# # def connect_db():
# #     return psycopg2.connect("dbname=lb8_users user=artematrr password=")

# # db = connect_db()
# # sessions = {}

# # class User:
# #     def __init__(self, user_id, name, age, password):
# #         self.id = user_id
# #         self.name = name
# #         self.age = age
# #         self.password = password

# # def generate_session_token():
# #     return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# # class RequestHandler(BaseHTTPRequestHandler):
# #     def _send_response(self, message, status_code=200):
# #         self.send_response(status_code)
# #         self.send_header('Content-Type', 'application/json')
# #         self.end_headers()
# #         self.wfile.write(json.dumps(message).encode('utf-8'))

# #     def do_POST(self):
# #         if self.path == '/login':
# #             self.handle_login()
# #         elif self.path == '/users':
# #             self.handle_create_user()
# #         else:
# #             self._send_response({'error': 'Неверный путь'}, 404)

# #     def handle_login(self):
# #         content_length = int(self.headers['Content-Length'])
# #         post_data = json.loads(self.rfile.read(content_length))
# #         name = post_data.get("name")
# #         password = post_data.get("password")

# #         with db.cursor() as cursor:
# #             cursor.execute("SELECT id, password FROM users WHERE name = %s", (name,))
# #             user = cursor.fetchone()

# #         if user and user[1] == password:
# #             token = generate_session_token()
# #             sessions[token] = user[0]  # ID пользователя
# #             self._send_response({'message': 'Авторизация успешна'}, 200)
# #             self.send_header('Authorization', token)
# #             self.end_headers()
# #         else:
# #             self._send_response({'error': 'Неправильное имя пользователя или пароль'}, 401)

# #     def handle_create_user(self):
# #         content_length = int(self.headers['Content-Length'])
# #         post_data = json.loads(self.rfile.read(content_length))
# #         name = post_data.get("name")
# #         age = post_data.get("age")
# #         password = post_data.get("password")

# #         errors = []
# #         if not name:
# #             errors.append("Имя не может быть пустым")
# #         if age is None or age <= 0:
# #             errors.append("Возраст должен быть положительным числом")

# #         if errors:
# #             self._send_response({'errors': errors}, 400)
# #             return

# #         with db.cursor() as cursor:
# #             cursor.execute("INSERT INTO users (name, age, password) VALUES (%s, %s, %s) RETURNING id",
# #                            (name, age, password))
# #             user_id = cursor.fetchone()[0]
# #             db.commit()

# #         self._send_response({'message': f'Пользователь создан с ID: {user_id}'}, 201)

# #     def do_GET(self):
# #         if self.path.startswith('/users'):
# #             self.handle_get_users()
# #         else:
# #             self._send_response({'error': 'Неверный путь'}, 404)

# #     def handle_get_users(self):
# #         with db.cursor() as cursor:
# #             cursor.execute("SELECT id, name, age FROM users")
# #             users = cursor.fetchall()

# #         user_list = [{'id': user[0], 'name': user[1], 'age': user[2]} for user in users]
# #         self._send_response(user_list)

# # def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
# #     server_address = ('', port)
# #     httpd = server_class(server_address, handler_class)
# #     print(f'Сервер запущен на порту {port}')
# #     httpd.serve_forever()

# # if __name__ == "__main__":
# #     run()

# 2
# import json
# import os
# import psycopg2
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import uuid

# DB_NAME = 'lb8_users'
# DB_USER = 'artematrr'
# DB_PASSWORD = ''
# DB_HOST = 'localhost'
# DB_PORT = '5432'

# class User:
#     def __init__(self, id, name, age, password):
#         self.id = id
#         self.name = name
#         self.age = age
#         self.password = password

# sessions = {}

# def connect_db():
#     conn = psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT
#     )
#     return conn

# def create_admin(conn):
#     with conn.cursor() as cur:
#         cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = 1);")
#         exists = cur.fetchone()[0]
#         if not exists:
#             cur.execute("INSERT INTO users (id, name, age, password) VALUES (1, 'admin', 30, 'admin');")
#             conn.commit()

# class RequestHandler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         if self.path == '/login':
#             self.authorize_user()
#         elif self.path == '/users':
#             self.create_user()
#         else:
#             self.send_response(404)
#             self.end_headers()

#     def do_GET(self):
#         if self.path == '/users':
#             self.get_users()
#         elif self.path.startswith('/users/'):
#             self.get_user_by_id()
#         else:
#             self.send_response(404)
#             self.end_headers()

#     def do_PUT(self):
#         if self.path.startswith('/users/'):
#             self.update_user()
#         else:
#             self.send_response(404)
#             self.end_headers()

#     def do_DELETE(self):
#         if self.path.startswith('/users/'):
#             self.delete_user()
#         else:
#             self.send_response(404)
#             self.end_headers()

#     def send_json_response(self, data, status=200):
#         self.send_response(status)
#         self.send_header('Content-Type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(data).encode())

#     def authorize_user(self):
#         content_length = int(self.headers['Content-Length'])
#         body = self.rfile.read(content_length)
#         user_data = json.loads(body)

#         with connect_db() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT id, password FROM users WHERE name = %s;", (user_data['name'],))
#                 result = cur.fetchone()
#                 if result and result[1] == user_data['password']:
#                     token = str(uuid.uuid4())
#                     sessions[token] = result[0]
#                     self.send_json_response({"message": "Авторизация успешна"}, 200)
#                     self.send_header('Authorization', token)
#                 else:
#                     self.send_json_response({"error": "Неправильное имя пользователя или пароль"}, 401)

# 2

#     def get_users(self):
#         with connect_db() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT id, name, age FROM users;")
#                 users = cur.fetchall()
#                 user_list = [{"id": user[0], "name": user[1], "age": user[2]} for user in users]
#                 self.send_json_response(user_list)

#     def get_user_by_id(self):
#         user_id = int(self.path.split('/')[-1])
#         with connect_db() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT id, name, age FROM users WHERE id = %s;", (user_id,))
#                 user = cur.fetchone()
#                 if user:
#                     self.send_json_response({"id": user[0], "name": user[1], "age": user[2]})
#                 else:
#                     self.send_json_response({"error": "Пользователь не найден"}, 404)

#     def create_user(self):
#         content_length = int(self.headers['Content-Length'])
#         body = self.rfile.read(content_length)
#         user_data = json.loads(body)

#         with connect_db() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("INSERT INTO users (name, age, password) VALUES (%s, %s, %s);",
#                             (user_data['name'], user_data['age'], user_data['password']))
#                 conn.commit()
#                 self.send_json_response({"message": "Пользователь создан"}, 201)

#     def update_user(self):
#         if not self.check_authorization():
#             self.send_json_response({"error": "Необходима авторизация"}, 401)
#             return

#         user_id = int(self.path.split('/')[-1])
#         content_length = int(self.headers['Content-Length'])
#         body = self.rfile.read(content_length)
#         user_data = json.loads(body)

#         with connect_db() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("UPDATE users SET name = %s, age = %s, password = %s WHERE id = %s;",
#                             (user_data['name'], user_data['age'], user_data['password'], user_id))
#                 conn.commit()
#                 self.send_json_response({"message": "Пользователь обновлен"}, 200)

#     def delete_user(self):
#         if not self.check_authorization():
#             self.send_json_response({"error": "Необходима авторизация"}, 401)
#             return

#         user_id = int(self.path.split('/')[-1])
#         with connect_db() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
#                 conn.commit()
#                 self.send_json_response({"message": "Пользователь удален"}, 200)

#     def check_authorization(self):
#         token = self.headers.get('Authorization')
#         return token in sessions

# def run(server_class=HTTPServer, handler_class=RequestHandler):
#     conn = connect_db()
#     create_admin(conn)
#     conn.close()

#     server_address = ('', 8080)
#     httpd = server_class(server_address, handler_class)
#     print('Сервер запущен на порту 8080...')
#     httpd.serve_forever()

# if __name__ == "__main__":
#     run()

import json
import os
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid

DB_NAME = 'lb8_users'
DB_USER = 'artematrr'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'

sessions = {}

def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def create_admin(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = 1);")
        exists = cur.fetchone()[0]
        if not exists:
            cur.execute("INSERT INTO users (id, name, age, password) VALUES (1, 'admin', 30, 'admin');")
            conn.commit()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/login':
            self.authorize_user()
        elif self.path == '/users':
            if self.check_authorization():
                self.create_user()
            else:
                self.send_json_response({"error": "Необходима авторизация"}, 401)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/users':
            if self.check_authorization():
                self.get_users()
            else:
                self.send_json_response({"error": "Необходима авторизация"}, 401)
        elif self.path.startswith('/users/'):
            if self.check_authorization():
                self.get_user_by_id()
            else:
                self.send_json_response({"error": "Необходима авторизация"}, 401)
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith('/users/'):
            if self.check_authorization():
                self.update_user()
            else:
                self.send_json_response({"error": "Необходима авторизация"}, 401)
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/users/'):
            if self.check_authorization():
                self.delete_user()
            else:
                self.send_json_response({"error": "Необходима авторизация"}, 401)
        else:
            self.send_response(404)
            self.end_headers()

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def authorize_user(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        user_data = json.loads(body)

        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, password FROM users WHERE name = %s;", (user_data['name'],))
                result = cur.fetchone()
                if result and result[1] == user_data['password']:
                    token = str(uuid.uuid4())
                    sessions[token] = result[0]
                    self.send_json_response({"message": "Авторизация успешна"}, 200)
                    self.send_header('Authorization', token)  # Move this line below send_json_response
                    self.end_headers()  # End headers after sending response
                else:
                    self.send_json_response({"error": "Неправильное имя пользователя или пароль"}, 401)

    def get_users(self):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, age FROM users;")
                users = cur.fetchall()
                user_list = [{"id": user[0], "name": user[1], "age": user[2]} for user in users]
                self.send_json_response(user_list)

    def get_user_by_id(self):
        user_id = int(self.path.split('/')[-1])
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, age FROM users WHERE id = %s;", (user_id,))
                user = cur.fetchone()
                if user:
                    self.send_json_response({"id": user[0], "name": user[1], "age": user[2]})
                else:
                    self.send_json_response({"error": "Пользователь не найден"}, 404)

    def create_user(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        user_data = json.loads(body)

        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (name, age, password) VALUES (%s, %s, %s);",
                            (user_data['name'], user_data['age'], user_data['password']))
                conn.commit()
                self.send_json_response({"message": "Пользователь создан"}, 201)

    def update_user(self):
        user_id = int(self.path.split('/')[-1])
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        user_data = json.loads(body)

        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET name = %s, age = %s, password = %s WHERE id = %s;",
                            (user_data['name'], user_data['age'], user_data['password'], user_id))
                conn.commit()
                self.send_json_response({"message": "Пользователь обновлен"}, 200)

    def delete_user(self):
        user_id = int(self.path.split('/')[-1])
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                conn.commit()
                self.send_json_response({"message": "Пользователь удален"}, 200)

    def check_authorization(self):
        token = self.headers.get('Authorization')
        return token in sessions


def run(server_class=HTTPServer, handler_class=RequestHandler):
    conn = connect_db()
    create_admin(conn)
    conn.close()

    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print('Сервер запущен на порту 8080...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()