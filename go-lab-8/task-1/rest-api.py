from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/users":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(users).encode())

        elif self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                user = next((u for u in users if u["id"] == user_id), None)
                if user:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(user).encode())
                else:
                    self.send_error(404, "Пользователь не найден")
            except ValueError:
                self.send_error(400, "Неверный ID")

    def do_POST(self):
        if self.path == "/users":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            user_data = json.loads(body)

            if "name" not in user_data:
                self.send_error(400, "Отсутствует обязательное поле 'name'")
                return

            user = {
                "id": len(users) + 1,
                "name": user_data["name"],
                "age": user_data.get("age", 0)
            }

            users.append(user)
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user).encode())

    def do_PUT(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                user = next((u for u in users if u["id"] == user_id), None)
                if not user:
                    self.send_error(404, "Пользователь не найден")
                    return

                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                updated_data = json.loads(body)

                user["name"] = updated_data.get("name", user["name"])
                user["age"] = updated_data.get("age", user["age"])

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(user).encode())
            except ValueError:
                self.send_error(400, "Неверный ID")

    def do_DELETE(self):
        if self.path.startswith("/users/"):
            try:
                user_id = int(self.path.split('/')[-1])
                global users
                new_users = [u for u in users if u["id"] != user_id]

                if len(new_users) == len(users):
                    self.send_error(404, "Пользователь не найден")
                else:
                    users = new_users
                    self.send_response(204)
                    self.end_headers()
            except ValueError:
                self.send_error(400, "Неверный ID")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту localhost:{port}")
    httpd.serve_forever()


users = [
    {"id": 1, "name": "Andrew", "age": 24},
]


if __name__ == '__main__':
    run()
