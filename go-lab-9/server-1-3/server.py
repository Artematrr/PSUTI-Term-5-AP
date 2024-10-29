import json
import psycopg2
from psycopg2 import sql
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class User:
    def __init__(self, user_id, name, age):
        self.id = user_id
        self.name = name
        self.age = age

def connect_db():
    conn = psycopg2.connect(
        dbname='lb8_users_test', 
        user='artematrr', 
        password='', 
        host='localhost', 
        port='5432'
    )
    return conn

class RequestHandler(BaseHTTPRequestHandler):
    db = connect_db()

    def _send_response(self, code, message=None):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if message is not None:
            self.wfile.write(json.dumps(message).encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        query_components = parse_qs(parsed_path.query)

        if len(path_parts) == 1 and path_parts[0] == 'users':
            self.get_users(query_components)
        elif len(path_parts) == 2 and path_parts[0] == 'users':
            self.get_user_by_id(path_parts[1])
        else:
            self._send_response(404, {"error": "Not found"})

    def get_users(self, query_components):
        limit = int(query_components.get('limit', [50])[0])
        offset = int(query_components.get('offset', [0])[0])
        name_filter = query_components.get('name', [''])[0]
        age_filter = query_components.get('age', [None])[0]

        query = "SELECT id, name, age FROM users WHERE TRUE"
        params = []

        if name_filter:
            query += " AND name ILIKE %s"
            params.append(f'%{name_filter}%')
        if age_filter:
            query += " AND age = %s"
            params.append(age_filter)

        query += " LIMIT %s OFFSET %s"
        params += [limit, offset]

        with self.db.cursor() as cur:
            cur.execute(query, params)
            users = cur.fetchall()
            response = [{"id": user[0], "name": user[1], "age": user[2]} for user in users]

        self._send_response(200, response)

    def get_user_by_id(self, user_id):
        with self.db.cursor() as cur:
            cur.execute("SELECT id, name, age FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            if user:
                response = {"id": user[0], "name": user[1], "age": user[2]}
                self._send_response(200, response)
            else:
                self._send_response(404, {"error": "User not found"})

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 1 and path_parts[0] == 'users':
            self.create_user()
        elif len(path_parts) == 2 and path_parts[0] == 'users':
            self.create_user_with_id(path_parts[1])
        else:
            self._send_response(404, {"error": "Not found"})

    def create_user(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data)

        name = user_data.get("name")
        age = user_data.get("age")

        if not name or age <= 0:
            self._send_response(400, {"error": "Invalid input"})
            return

        with self.db.cursor() as cur:
            cur.execute("INSERT INTO users (name, age) VALUES (%s, %s) RETURNING id", (name, age))
            user_id = cur.fetchone()[0]
            self.db.commit()

        self._send_response(201, {"id": user_id, "name": name, "age": age})

    def create_user_with_id(self, user_id):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data)

        name = user_data.get("name")
        age = user_data.get("age")

        if not name or age <= 0:
            self._send_response(400, {"error": "Invalid input"})
            return

        with self.db.cursor() as cur:
            cur.execute("INSERT INTO users (id, name, age) VALUES (%s, %s, %s)", (user_id, name, age))
            self.db.commit()

        self._send_response(201, {"id": user_id, "name": name, "age": age})

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 2 and path_parts[0] == 'users':
            self.update_user(path_parts[1])
        else:
            self._send_response(404, {"error": "Not found"})

    def update_user(self, user_id):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data)

        name = user_data.get("name")
        age = user_data.get("age")

        if not name or age <= 0:
            self._send_response(400, {"error": "Invalid input"})
            return

        with self.db.cursor() as cur:
            cur.execute("UPDATE users SET name = %s, age = %s WHERE id = %s", (name, age, user_id))
            self.db.commit()

        self._send_response(200, {"id": user_id, "name": name, "age": age})

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 2 and path_parts[0] == 'users':
            self.delete_user(path_parts[1])
        else:
            self._send_response(404, {"error": "Not found"})

    def delete_user(self, user_id):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db.commit()

        self._send_response(204)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()