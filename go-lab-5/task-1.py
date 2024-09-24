import math


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return f"Звать {self.name}, {self.age} лет"


def task1():
    print("\n>> Задача 1")

    print(person.get_info())


def task2():
    print("\n>> Задача 2")
    print("С днюшечкой!!")
    person.age += 1
    print(person.get_info())


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return self.radius * self.radius * math.pi


def task3():
    print("\n>> Задача 3")
    print(f"Площадь круга: {circle.area():.2f}")


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


def task4():
    print("\n>> Задача 4")
    print("Площади:")
    for shape in shapes:
        print(f"{shape.area():.2f}")


def slice_shapes(shapes):
    for shape in shapes:
        print(f"{shape.area():.2f}")


def task5():
    print("\n>> Задача 5")
    print("Те же площади, но функцией:")
    slice_shapes(shapes)


class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

    def get_info(self):
        return f"«{self.title}» от автора {self.author} ({self.genre})"


def task6():
    print("\n>> Задача 6")
    print("Книжная инфа:")

    print(book.get_info())


def main():
    global person, circle, shapes, book

    person = Person("Артем", 20)

    circle = Circle(12.5)

    shapes = [
        Circle(17),
        Rectangle(20.2, 7)
    ]

    book = Book("Война и мир", "Лев Николаевич Толстой", "Роман")

    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()
