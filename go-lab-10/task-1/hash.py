import hashlib

def hash_string(hash_func, input_string):
    if hash_func == 'md5':
        return hashlib.md5(input_string.encode()).hexdigest()
    elif hash_func == 'sha256':
        return hashlib.sha256(input_string.encode()).hexdigest()
    elif hash_func == 'sha512':
        return hashlib.sha512(input_string.encode()).hexdigest()
    else:
        print("Неизвестная функция хэширования")
        return None

def main():
    input_string = input("Введите строку для хэширования: ")
    
    print("Выберите хэш-функцию:")
    print("1. MD5")
    print("2. SHA-256")
    print("3. SHA-512")
    choice = int(input("Введите номер выбора: "))
    
    if choice == 1:
        hash_func = 'md5'
    elif choice == 2:
        hash_func = 'sha256'
    elif choice == 3:
        hash_func = 'sha512'
    else:
        print("Некорректный выбор")
        return

    hashed = hash_string(hash_func, input_string)
    print(f"Хэш: {hashed}")

    check_string = input("Введите строку для проверки целостности: ")
    check_hash = input("Введите хэш для проверки: ")

    if hash_string(hash_func, check_string) == check_hash:
        print("Целостность данных подтверждена.")
    else:
        print("Целостность данных опровергнута.")

if __name__ == "__main__":
    main()