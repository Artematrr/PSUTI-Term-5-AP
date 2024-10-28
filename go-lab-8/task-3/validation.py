import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="lb8_users",
            user="artematrr",
            password="",  # Укажите пароль, если требуется
            host="localhost"
        )
        return conn
    except psycopg2.DatabaseError as e:
        raise Exception(f"Ошибка при подключении к базе данных: {e}")


# Функция для валидации данных пользователя
def validate_user_data(data):
    if "name" not in data or not isinstance(data["name"], str) or not data["name"].strip():
        raise ValueError("Pole 'name' ne mojet bit pustym.")
    if "age" in data and (not isinstance(data["age"], int) or data["age"] < 0):
        raise ValueError("Pole 'age' doljnogo bit polozhitelnym chislom.")


class RequestHandler(BaseHTTPRequestHandler):

    def send_json_response(self, code, data=None):
        """Упрощенная отправка JSON-ответов"""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    # Получение списка пользователей (GET /users)
    def do_GET(self):
        if self.path == "/users":
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users;")
                users = cursor.fetchall()
                cursor.close()
                conn.close()

                user_list = [{"id": row[0], "name": row[1], "age": row[2]} for row in users]
                self.send_json_response(200, user_list)

            except Exception as e:
                self.send_json_response(500, {"error": f"Серверная ошибка: {e}"})

        elif self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()

                if user:
                    user_data = {"id": user[0], "name": user[1], "age": user[2]}
                    self.send_json_response(200, user_data)
                else:
                    self.send_json_response(404, {"error": "Пользователь не найден"})

            except ValueError:
                self.send_json_response(400, {"error": "Invalid ID"})
            except Exception as e:
                self.send_json_response(500, {"error": f"Серверная ошибка: {e}"})

    # Добавление нового пользователя (POST /users)
    def do_POST(self):
        if self.path == "/users":
            try:
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                user_data = json.loads(body)

                # Сама валидация
                validate_user_data(user_data)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, age) VALUES (%s, %s) RETURNING id;",
                    (user_data["name"], user_data.get("age", 0))
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()

                user_data["id"] = user_id
                self.send_json_response(201, user_data)

            except ValueError as e:
                self.send_json_response(400, {"error": str(e)})
            except Exception as e:
                self.send_json_response(500, {"error": f"Серверная ошибка: {e}"})

    # Обновление информации о пользователе (PUT /users/{id})
    def do_PUT(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                updated_data = json.loads(body)

                # Валидация данных
                validate_user_data(updated_data)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
                user = cursor.fetchone()

                if not user:
                    self.send_json_response(404, {"error": "Пользователь не найден"})
                    return

                cursor.execute(
                    "UPDATE users SET name = %s, age = %s WHERE id = %s;",
                    (updated_data.get("name", user[1]), updated_data.get("age", user[2]), user_id)
                )
                conn.commit()
                cursor.close()
                conn.close()

                self.send_json_response(200, {"id": user_id, "name": updated_data.get("name", user[1]),
                                               "age": updated_data.get("age", user[2])})

            except ValueError as e:
                self.send_json_response(400, {"error": str(e)})
            except Exception as e:
                self.send_json_response(500, {"error": f"Серверная ошибка: {e}"})

    # Удаление пользователя (DELETE /users/{id})
    def do_DELETE(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
                deleted_id = cursor.fetchone()
                conn.commit()
                cursor.close()
                conn.close()

                if deleted_id:
                    self.send_response(204)
                    self.end_headers()
                else:
                    self.send_json_response(404, {"error": "Пользователь не найден"})

            except ValueError:
                self.send_json_response(400, {"error": "Invalid ID"})
            except Exception as e:
                self.send_json_response(500, {"error": f"Серверная ошибка: {e}"})


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту localhost:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()