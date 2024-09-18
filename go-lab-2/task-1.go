package main

import (
	"fmt"
)

func main() {
	Task1()
	Task2()
	Task3()
	Task4()
	Task5()
	Task6()
}

func isEven(n int) string {
	even := n%2 == 0
	if even {
		return "Чётное"
	} else {
		return "Нечётное"
	}
}

func Task1() {
	fmt.Println("\n>> Задача 1")

	var num int
	fmt.Print("Введите введите число: ")
	fmt.Scan(&num)

	fmt.Println(isEven(num))
}

func Task2() {
	fmt.Println("\n>> Задача 2")

	var num int
	fmt.Print("Введите введите число: ")
	fmt.Scan(&num)

	if num > 0 {
		fmt.Println("Positive")
	} else if num < 0 {
		fmt.Println("Negative")
	} else {
		fmt.Println("Zero")
	}
}

func Task3() {
	fmt.Println("\n>> Задача 3")

	for i := 1; i <= 10; i++ {
		fmt.Print(i, " ")
	}
	fmt.Println()
}

func Task4() {
	fmt.Println("\n>> Задача 4")

	var str string
	fmt.Print("Введите строку: ")
	fmt.Scan(&str)

	fmt.Println("Длина строки: ", len(str))
}

// Task5

// передача с указателем на структуру, чтобы не создавать копию и иметь возм. изменять значения полей (в случае чего, здесь не продемонстрируем)
func rectangleArea(r *Rectangle) int {
	return r.width * r.height
}

type Rectangle struct {
	width, height int
}

func Task5() {
	fmt.Println("\n>> Задача 5")

	// Экземпляр двумя способами
	// rect := Rectangle{}
	var rect Rectangle

	fmt.Print("Введите длину прямоугольника:\t")
	fmt.Scan(&rect.width)
	fmt.Print("Введите высоту прямоугольника:\t")
	fmt.Scan(&rect.height)

	fmt.Print("Площадь прямоугольника:\t\t", rectangleArea(&rect))
	println()
}

func Task6() {
	fmt.Println("\n>> Задача 6")

	var (
		a, b int64
		c    float64
	)

	fmt.Print("Введите первое число:\t")
	fmt.Scan(&a)
	fmt.Print("Введите второе число:\t")
	fmt.Scan(&b)

	c = float64(a+b) / 2
	fmt.Print("Среднее арифметическое:\t", c)
	fmt.Println()

}
