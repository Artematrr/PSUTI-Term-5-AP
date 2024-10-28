import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Подключение к базе данных


def get_db_connection():
    conn = psycopg2.connect(
        dbname="lb8_users_test",
        user="artematrr",
        password="",
        host="localhost"
    )
    return conn


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/users":
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            cursor.close()
            conn.close()

            user_list = [{"id": row[0], "name": row[1], "age": row[2]}
                         for row in users]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user_list).encode())

        elif self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE id = %s;", (user_id,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()

                if user:
                    user_data = {"id": user[0],
                                 "name": user[1], "age": user[2]}
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(user_data).encode())
                else:
                    self.send_error(404, "User not found")
            except ValueError:
                self.send_error(400, "Invalid ID")

    def do_POST(self):
        if self.path == "/users":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            user_data = json.loads(body)

            if "name" not in user_data:
                self.send_error(400, "Missing name field")
                return

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

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user_data).encode())

    def do_PUT(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                updated_data = json.loads(body)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE id = %s;", (user_id,))
                user = cursor.fetchone()

                if not user:
                    self.send_error(404, "User not found")
                    cursor.close()
                    conn.close()
                    return

                cursor.execute(
                    "UPDATE users SET name = %s, age = %s WHERE id = %s;",
                    (updated_data.get("name", user[1]), updated_data.get(
                        "age", user[2]), user_id)
                )
                conn.commit()
                cursor.close()
                conn.close()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"id": user_id, "name": updated_data.get(
                    "name", user[1]), "age": updated_data.get("age", user[2])}).encode())

            except ValueError:
                self.send_error(400, "Invalid ID")

    def do_DELETE(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
                deleted_id = cursor.fetchone()
                conn.commit()
                cursor.close()
                conn.close()

                if deleted_id:
                    self.send_response(204)
                    self.end_headers()
                else:
                    self.send_error(404, "User not found")

            except ValueError:
                self.send_error(400, "Invalid ID")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту localhost:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
