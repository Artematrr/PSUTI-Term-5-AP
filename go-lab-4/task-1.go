package main

import (
	f "fmt"
	m "math"
	"strconv"
	"strings"
)

func task1() {
	f.Println("\n>> Задача 1")

	f.Println("Текущие люди: ", people)

	f.Print("Добавьте человека (имя): ")
	var name string
	f.Scan(&name)

	f.Print("Добавьте его возраст (в годах): ")
	var age int
	f.Scan(&age)

	people[name] = age

	f.Println("Все люди: ", people)
}

func roundFloat(val float64, precision uint) float64 {
	ratio := m.Pow(10, float64(precision))
	return m.Round(val*ratio) / ratio
}

func averAge(people map[string]int) float64 {
	var sum int
	for _, value := range people {
		sum += value
	}
	average := roundFloat(float64(sum)/float64(len(people)), 2)
	return average
}

func task2() {
	f.Println("\n>> Задача 1")

	f.Println("Средний возsраст: ", averAge(people))
}

func task3() {
	f.Println("\n>> Задача 3")

	f.Print("Введите имя человека, которого надо удалить: ")
	var name string
	f.Scan(&name)

	delete(people, name)
	f.Println("Текущие люди: ", people)
}

func task4() {
	f.Println("\n>> Задача 4")

	f.Print("Введите строку:\t\t")
	var str string
	f.Scan(&str)

	str = strings.ToUpper(str)
	f.Print("В верхнем регистре:\t", str)
	f.Println()
}

func task5() {
	f.Println("\n>> Задача 5")

	f.Print("Сколько чисел сложить: ")
	var n int
	f.Scan(&n)

	var sum int
	for i := 0; i < n; i++ {
		var num int
		f.Scan(&num)
		sum += num
	}
	f.Println("Сумма чисел: ", sum)
}

func task6() {
	f.Println("\n>> Задача 6")

	f.Print("Сколько чисел обратить: ")
	var n int
	f.Scan(&n)

	str := ""
	for i := 0; i < n; i++ {
		var num int
		f.Scan(&num)
		str = strconv.Itoa(num) + " " + str
	}

	f.Println("В обратном порядке: ", str)
}

var people = map[string]int{
	"Артем":   20,
	"Андрей":  31,
	"Типур":   32,
	"Мария":   18,
	"Евгения": 21,
}

func main() {
	task1()
	task2()
	task3()
	task4()
	task5()
	task6()
}
