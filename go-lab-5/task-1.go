package main

import (
	f "fmt"
	m "math"
)

func (person *Person) getInfo() string {
	return f.Sprintf("Звать %s, %d лет", person.name, person.age)
}

type Person struct {
	name string
	age  int
}

func task1() {
	f.Println("\n>> Задача 1")

	f.Println(person.getInfo())
}

//

func (person *Person) birthday() {
	person.age++
}

func task2() {
	f.Println("\n>> Задача 2")

	f.Println("С днюшечкой!!")
	person.birthday()

	f.Println(person.getInfo())
}

//

func (circle *Circle) Area() float64 {
	return circle.radius * circle.radius * m.Pi
}

type Circle struct {
	radius float64
}

func task3() {
	f.Println("\n>> Задача 3")

	f.Printf("Площадь круга: %.2f\n", circle.Area())
}

//

func (r *Rectangle) Area() float64 {
	return r.width * r.height
}

type Rectangle struct {
	width, height float64
}

type Shape interface {
	Area() float64
}

func task4() {
	f.Println("\n>> Задача 4")

	f.Println("Площади:")
	for _, shape := range shapes {
		f.Printf("%.2f\n", shape.Area())
	}
}

func sliceShapes(shapes []Shape) {
	for _, shape := range shapes {
		f.Printf("%.2f\n", shape.Area())
	}
}

func task5() {
	f.Println("\n>> Задача 5")

	f.Println("Те же площади, но функцией:")
	sliceShapes(shapes)
}

//

func (book *Book) getInfo() string {
	return f.Sprintf("«‎%s» от автора %s (%s)",
		book.title, book.author, book.genre)
}

type Stringer interface {
	getInfo() string
}

type Book struct {
	title  string
	author string
	genre  string
}

func task6() {
	f.Println("\n>> Задача 6")

	f.Println("Книжная инфа:")
	book := Book{
		title:  "Война и мир",
		author: "Лев Николаевич Толстой",
		genre:  "Роман",
	}
	f.Println(book.getInfo())
}

//

var person = Person{
	name: "Артем",
	age:  20,
}

var circle = Circle{
	radius: 12.5,
}

var shapes = []Shape{
	&Circle{radius: 17},
	&Rectangle{width: 20.2, height: 7}}

func main() {
	task1()
	task2()
	task3()
	task4()
	task5()
	task6()

}
