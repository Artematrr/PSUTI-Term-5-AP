import socket
import ssl


def tcp_tls_client():
    host = 'localhost'
    port = 8080

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        with context.wrap_socket(client_socket, server_hostname=host) as tls_socket:
            tls_socket.connect((host, port))
            message = input("Введите сообщение для отправки: ")
            tls_socket.send(message.encode())
            response = tls_socket.recv(1024).decode()
            print("Ответ сервера:", response)


if __name__ == "__main__":
    tcp_tls_client()
