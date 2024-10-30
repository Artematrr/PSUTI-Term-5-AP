import rsa


def generate_keys():
    (pubkey, privkey) = rsa.newkeys(2048)
    with open('public_key.pem', 'wb') as pub_file:
        pub_file.write(pubkey.save_pkcs1('PEM'))
    with open('private_key.pem', 'wb') as priv_file:
        priv_file.write(privkey.save_pkcs1('PEM'))
    print("Ключи успешно сгенерированы и сохранены в файлы.")


def sign_message(message):
    with open('private_key.pem', 'rb') as priv_file:
        privkey = rsa.PrivateKey.load_pkcs1(priv_file.read())
    signature = rsa.sign(message.encode(), privkey, 'SHA-1')
    with open('signature.sig', 'wb') as sig_file:
        sig_file.write(signature)
    print("Сообщение успешно подписано и подпись сохранена в файл signature.sig.")


def verify_signature(message):
    with open('signature.sig', 'rb') as sig_file:
        signature = sig_file.read()
    with open('public_key.pem', 'rb') as pub_file:
        pubkey = rsa.PublicKey.load_pkcs1(pub_file.read())
    try:
        rsa.verify(message.encode(), signature, pubkey)
        print("Подпись действительна.")
    except rsa.VerificationError:
        print("Подпись недействительна.")


def main():

    print("Выберите действие:")
    print("1. Сгенерировать ключи")
    print("2. Подписать сообщение")
    print("3. Проверить подпись")
    choice = int(input())

    if choice == 1:
        generate_keys()
    elif choice == 2:
        message = input("Подписать сообщегие: ")
        sign_message(message)
    elif choice == 3:
        message = input("Проверить подпись сообщения: ")
        verify_signature(message)
    else:
        print("Некорректный выбор.")


if __name__ == "__main__":
    while True:
        main()
