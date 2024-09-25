from mathutils import factorial
from stringutils import reverse_row


def task2():
    print("\n>> Задача 2")
    num = int(input("Введите число для нахождения его факториала: "))
    print(factorial(num))


def task3():
    print("\n>> Задача 3")
    s = input("Введите строку: ")
    print(reverse_row(s))


def task4():
    print("\n>> Задача 4")
    arr = list(range(5))
    print("Массив:", arr)


def task5():
    print("\n>> Задача 5")
    arr = list(range(1, 11))
    print("Массив:\t\t", arr)
    slice = arr[2:6]
    print("Срез:\t\t", slice)
    slice.extend([11, 12, 13])
    print("Добавление:\t", slice)
    slice.pop()
    print("Удаление:\t", slice)


def task6():
    print("\n>> Задача 6")
    arr = ["яблочко", "банан", "вишня", "груша", "дыня", "ежемалина"]
    print("Массив строк:\t", arr)
    max_str = max(arr, key=len)
    print("Длиннющая:\t", max_str)
    slice = arr[:3]
    print("Срез:\t\t", slice)
    max_str_slice = max(slice, key=len)
    print("Длиннющая:\t", max_str_slice)


def main():
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()
