import math


def task1():
    print("\n>> Задача 1")

    print("Текущие люди:", people)

    name = input("Добавьте человека (имя): ")
    age = int(input("Добавьте его возраст (в годах): "))

    people[name] = age

    print("Все люди:", people)


def round_float(val, precision):
    ratio = 10**precision
    return round(val * ratio) / ratio


def average_age(people):
    total_age = sum(people.values())
    average = round_float(total_age / len(people), 2)
    return average


def task2():
    print("\n>> Задача 2")
    print("Средний возраст:", average_age(people))


def task3():
    print("\n>> Задача 3")

    name = input("Введите имя человека, которого надо удалить: ")
    if name in people:
        del people[name]
    print("Текущие люди:", people)


def task4():
    print("\n>> Задача 4")

    s = input("Введите строку: ")
    print("В верхнем регистре:", s.upper())


def task5():
    print("\n>> Задача 5")

    n = int(input("Сколько чисел сложить: "))
    total = 0
    for i in range(n):
        num = int(input())
        total += num
    print("Сумма чисел:", total)


def task6():
    print("\n>> Задача 6")

    n = int(input("Сколько чисел обратить: "))
    nums = [int(input()) for _ in range(n)]
    print("В обратном порядке:", " ".join(map(str, reversed(nums))))


people = {"Артем": 20,
          "Андрей": 31,
          "Типур": 32,
          "Мария": 18,
          "Евгения": 21}


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()
