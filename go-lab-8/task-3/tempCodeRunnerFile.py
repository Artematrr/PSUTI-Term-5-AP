te_user_data(data):
    if "name" not in data or not isinstance(data["name"], str) or not data["name"].strip():
        raise ValueError("Поле 'name' не может быть пустым.")
    if "age" in data and (not isinstance(data["age"], int) or data["age"] < 0):
        raise ValueError("Поле 'age' должно быть положительным числом.")

