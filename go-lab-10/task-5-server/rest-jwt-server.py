import json
import jwt
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

users = [
    {"id": 1, "name": "Андрейка", "age": 24, "role": "user"},
    {"id": 2, "name": "Admin", "age": 30, "role": "admin"}
]
SECRET_KEY = "privet"

def generate_jwt(user):
    payload = {
        "user_id": user["id"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if self.path == "/login":
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                data = json.loads(body)
                user = next((u for u in users if u["name"] == data["name"]), None)
                if user:
                    token = generate_jwt(user)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"token": token}).encode())
                else:
                    self.send_error(401, "Пользователь не найден")
            
            elif self.path == "/users":
                content_length = int(self.headers["Content-Length"])
                body = self.rfile.read(content_length)
                data = json.loads(body)
                token = self.headers.get("Authorization")
                if not token:
                    self.send_error(401, "Токен отсутствует")
                    return

                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    role = payload["role"]
                    if role != "admin":
                        self.send_error(403, "Недостаточно прав для добавления пользователя")
                        return

                    new_user = {
                        "id": len(users) + 1,
                        "name": data["name"],
                        "age": data["age"],
                        "role": data["role"]
                    }
                    users.append(new_user)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(new_user).encode())
                except jwt.InvalidTokenError:
                    self.send_error(401, "Неверный токен")

        except json.JSONDecodeError:
            self.send_error(400, "Ошибка обработки JSON")
        except Exception as e:
            self.send_error(500, f"Внутренняя ошибка сервера: {str(e)}")

    def do_GET(self):
        try:
            if self.path == "/users":
                token = self.headers.get("Authorization")
                if not token:
                    self.send_error(401, "Токен отсутствует")
                    return

                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    role = payload["role"]

                    if role not in ["user", "admin"]:
                        self.send_error(403, "Недостаточно прав")
                        return

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(users).encode())
                except jwt.ExpiredSignatureError:
                    self.send_error(401, "Токен истек")
                except jwt.InvalidTokenError:
                    self.send_error(401, "Неверный токен")
        
        except Exception as e:
            self.send_error(500, f"Внутренняя ошибка сервера: {str(e)}")

def run():
    server = HTTPServer(('', 8080), RequestHandler)
    print("Сервер запущен на порту localhost:8080")
    server.serve_forever()

if __name__ == "__main__":
    run()