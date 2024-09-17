package main

import (
	"fmt"
	"time"
)

func main() {
	Task1()
	Task2()
	Task3()
	Task4()
	Task5()
	Task6()
}

func Task1() {
	fmt.Println("\n>> Задача 1")

	now := time.Now()
	fmt.Println("Текущее время с датой:", now.Format("15:04:05, 02.01.2006"))
}

func Task2() {
	fmt.Println("\n>> Задача 2")

	var a int
	var b float64
	var c string
	var d bool
	fmt.Println(a, b, c, d)
}

func Task3() {
	fmt.Println("\n>> Задача 3")

	a1 := 10
	b1 := 3.14
	c1 := "Привки!"
	d1 := true
	fmt.Println(a1, b1, c1, d1)
}

func Task4() {
	fmt.Println("\n>> Задача 4")

	var a int = 10
	var b int = 5

	fmt.Println(a+b, a-b, a*b, a/b)

}

func Task5() {
	fmt.Println("\n>> Задача 5")

	var a float64 = 10.4
	var b float64 = 5.2

	fmt.Println(a+b, a-b, a*b, a/b)
}

func Task6() {
	fmt.Println("\n>> Задача 6")

	var a, b, c int
	a = 10
	b = 4
	c = 7

	fmt.Println(aver(a, b, c))
}

func aver(a int, b int, c int) int {
	var sum int = a + b + c
	return sum

}
