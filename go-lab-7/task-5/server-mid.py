from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time


def log_request(method, path, duration):
    print(f"Метод: {method}, URL: {path}, Время: {duration:.4f} сек")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        start_time = time.time()

        if self.path == '/hello':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Zdorovenki buly")
        else:
            self.send_response(404)
            self.end_headers()

        log_request(self.command, self.path, time.time() -
                    start_time)

    def do_POST(self):
        start_time = time.time()

        if self.path == '/data':
            content_length = int(self.headers.get('Content-Length', 0))

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)  # Преобразуем JSON в Python-объект
            print(f"Полученные данные: {data}")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write("Данные успешно доставлены!!!!!!!".encode())
        else:
            self.send_response(404)
            self.end_headers()

        log_request(self.command, self.path, time.time() -
                    start_time)


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("HTTP-сервер middleware запущен и внимает порту 8080...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
