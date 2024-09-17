def is_even(n):
    return "Чётное" if n % 2 == 0 else "Нечётное"


def task1():
    print("\n>> Задача 1")
    num = int(input("Введите число: "))
    print(is_even(num))


def task2():
    print("\n>> Задача 2")
    num = int(input("Введите число: "))
    if num > 0:
        print("Positive")
    elif num < 0:
        print("Negative")
    else:
        print("Zero")


def task3():
    print("\n>> Задача 3")
    for i in range(1, 11):
        print(i, end=" ")
    print()


def task4():
    print("\n>> Задача 4")
    string = input("Введите строку: ")
    print("Длина строки: ", len(string))


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


def task5():
    print("\n>> Задача 5")
    width = int(input("Введите длину прямоугольника: "))
    height = int(input("Введите высоту прямоугольника: "))
    rect = Rectangle(width, height)
    print("Площадь прямоугольника: ", rect.area())


def task6():
    print("\n>> Задача 6")
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))
    avg = (a + b) / 2
    print("Среднее арифметическое: ", avg)


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()
