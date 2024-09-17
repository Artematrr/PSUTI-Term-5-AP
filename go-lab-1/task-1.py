import datetime


def task1():
    print("\n>> Задача 1")
    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()
    print("Текущее время с датой:", time, date)


def task2():
    print("\n>> Задача 2")
    a = 10
    b = 3.14
    c = "Привки!"
    d = True
    print(a, b, c, d)


def task3():
    print("\n>> Задача 3")
    a = 10
    b = 3.14
    c = "Привки!"
    d = True
    print(a, b, c, d)


def task4():
    print("\n>> Задача 4")
    a = 10
    b = 5
    print(a + b, a - b, a * b, a // b)


def task5():
    print("\n>> Задача 5")
    a = 10.4
    b = 5.2
    print(a + b, a - b, a * b, a / b)


def task6():
    print("\n>> Задача 6")
    a, b, c = 10, 4, 7
    print(aver(a, b, c))


def aver(a, b, c):
    return a + b + c


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()
