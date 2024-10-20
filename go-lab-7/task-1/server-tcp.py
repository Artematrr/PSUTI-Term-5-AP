import socket

def tcp_server():
    host = 'localhost'
    port = 8080
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"TCP-сервер запущен и внимает порту {host}:{port}")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Адрес сервера: {addr}")
        
        message = conn.recv(1024).decode()
        if message:
            print(f"Полученное сообщение: {message}")
            conn.send("Сообщение успешно доставлено".encode())
        
        conn.close()

if __name__ == "__main__":
    tcp_server()