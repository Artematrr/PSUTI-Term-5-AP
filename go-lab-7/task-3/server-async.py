import socket
import threading


def handle_client(conn, addr):
    print(f"Адрес подключения: {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Получно: {data.decode()}")
        conn.sendall("Сообщение успешно доставлено".encode())

    conn.close()


def tcp_server_async():
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"TCP-сервер запущен и внимает порту {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("\nСервер безопасно остановлен")
        server_socket.close()


if __name__ == "__main__":
    tcp_server_async()
