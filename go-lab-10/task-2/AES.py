
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


def encrypt(plain_text, key):

    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)

    padded_text = pad(plain_text.encode('utf-8'), AES.block_size)

    cipher_text = cipher.encrypt(padded_text)

    return base64.b64encode(cipher.iv + cipher_text).decode('utf-8')


def decrypt(cipher_text, key):

    cipher_bytes = base64.b64decode(cipher_text)

    iv = cipher_bytes[:AES.block_size]
    cipher_bytes = cipher_bytes[AES.block_size:]

    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

    decrypted_text = unpad(cipher.decrypt(cipher_bytes), AES.block_size)

    return decrypted_text.decode('utf-8')


def main():
    input_string = input("Введите строку для шифрования: ")
    key = input("Введите секретный ключ (16, 24 или 32 байта): ")

    encrypted = encrypt(input_string, key)
    print(f"Зашифрованный текст: {encrypted}")

    cipher_text = input("Введите зашифрованный текст для расшифрования: ")
    decrypted = decrypt(cipher_text, key)
    # cipher_pattern = input("Введите ключ шифрования: ")
    # decrypted = decrypt(cipher_text, cipher_pattern)
    print(f"Расшифрованный текст: {decrypted}")


if __name__ == "__main__":
    main()
