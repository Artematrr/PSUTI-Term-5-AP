import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# Подключение к базе данных


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


class RequestHandler(BaseHTTPRequestHandler):

    def send_json_response(self, code, data=None):
        """Упрощенная отправка JSON-ответов"""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())

    # Получение списка пользователей (GET /users) с поддержкой пагинации и фильтрации
    def do_GET(self):
        if self.path.startswith("/users"):
            try:
                # Разбираем параметры запроса
                url_parts = urlparse(self.path)
                query_params = parse_qs(url_parts.query)

                # Параметры фильтрации
                name_filter = query_params.get("name", [None])[0]
                age_filter = query_params.get("age", [None])[0]
                if age_filter is not None:
                    age_filter = int(age_filter)

                # Параметры пагинации
                # По умолчанию 10 пользователей
                limit = int(query_params.get("limit", [10])[0])
                offset = int(query_params.get("offset", [0])[
                             0])  # По умолчанию без смещения

                conn = get_db_connection()
                cursor = conn.cursor()

                # Построение SQL-запроса с фильтрацией
                base_query = "SELECT * FROM users"
                conditions = []
                values = []

                if name_filter:
                    conditions.append("name ILIKE %s")
                    # Используем LIKE для поиска по подстроке
                    values.append(f"%{name_filter}%")

                if age_filter is not None:
                    conditions.append("age = %s")
                    values.append(age_filter)

                if conditions:
                    base_query += " WHERE " + " AND ".join(conditions)

                base_query += " LIMIT %s OFFSET %s"
                values.extend([limit, offset])

                cursor.execute(base_query, tuple(values))
                users = cursor.fetchall()
                cursor.close()
                conn.close()

                user_list = [{"id": row[0], "name": row[1], "age": row[2]}
                             for row in users]

                self.send_json_response(200, user_list)

            except ValueError:
                self.send_error(400, "Неверные параметры для фильтрации или пагинации")
            except Exception as e:
                self.send_error(500, f"Ошибка сервера: {e}")

    # Остальные методы (POST, PUT, DELETE) остаются без изменений...


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту localhost:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
