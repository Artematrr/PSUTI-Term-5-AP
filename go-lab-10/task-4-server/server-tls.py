import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta, timezone

def generate_self_signed_cert():
    # Генерируем закрытый ключ
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Создаем самоподписанный сертификат
    subject = issuer = x509.Name([
        x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, u"My Organization"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(tz=timezone.utc)
    ).not_valid_after(
        datetime.now(tz=timezone.utc) + timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Сохраняем сертификат и ключ
    with open("server-py.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # Сохраняем закрытый ключ без шифрования
    with open("server-py.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # Исправлено: добавлен NoEncryption
        ))

def tcp_tls_server():
    host = 'localhost'
    port = 8080

    # generate_self_signed_cert()  # Генерация сертификата
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.crt', keyfile='server-py.key')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"TLS-сервер запущен и внимает порту {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        with context.wrap_socket(conn, server_side=True) as tls_conn:
            print(f"Подключен адрес: {addr}")
            message = tls_conn.recv(1024).decode()
            if message:
                print(f"Полученное сообщение: {message}")
                tls_conn.send("Сообщение успешно доставлено".encode())

if __name__ == "__main__":
    tcp_tls_server()