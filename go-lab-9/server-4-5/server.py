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
            self.create_user()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/users':
            self.get_users()
        elif self.path.startswith('/users/'):
            self.get_user_by_id()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith('/users/'):
            self.update_user()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/users/'):
            self.delete_user()
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