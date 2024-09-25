package main

import (
	f "fmt"
)

func main() {
	Task2()
	Task3()
	Task4()
	Task5()
	Task6()
}

func Task2() {
	f.Println("\n>> Задача 2")

	var num int
	f.Print("Введите для нахождения его факториала: ")
	f.Scan(&num)

	f.Println(Factorial(num))
}

func Task3() {
	f.Println("\n>> Задача 3")

	var str string
	f.Print("Введите строку: ")
	f.Scan(&str)

	f.Println(reverseRow(str))
}

func Task4() {
	f.Println("\n>> Задача 4")

	var arr [5]int
	// f.Println("Введите 5 целых чисел: ")
	// f.Scan(&arr[0], &arr[1], &arr[2], &arr[3], &arr[4])
	for i := 0; i < 5; i++ {
		arr[i] = i
	}
	f.Println("Массив: ", arr)
}

func Task5() {
	f.Println("\n>> Задача 5")

	var arr = [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	f.Println("Массив:\t\t", arr)

	var slice = arr[2:6]
	f.Println("Срез:\t\t", slice)

	slice = append(slice, 11, 12, 13)
	f.Println("Добавление:\t", slice)

	// slice[len(slice)-1] = ""  // 2. Удалить последний элемент (записать нулевое значение).
	// slice = slice[:len(slice)-1]  // 3. Усечь срез.

	slice = slice[:len(slice)-1]
	f.Println("Удаление:\t", slice)
}

func Task6() {
	f.Println("\n>> Задача 6")

	var arr = []string{"яблочко", "банан", "вишня", "груша", "дыня", "ежемалина"}
	f.Println("Массив строк:\t", arr)

	var maxStr = arr[0]
	for i := 1; i < len(arr); i++ {
		if len(arr[i]) > len(maxStr) {
			maxStr = arr[i]
		}
	}
	f.Println("Длиннющая:\t", maxStr)

	slice := arr[:3]
	f.Println("Срез:\t\t", slice)

	var maxStrSlice = slice[0]
	for i := 1; i < len(slice); i++ {
		if len(slice[i]) > len(maxStrSlice) {
			maxStrSlice = slice[i]
		}
	}

	f.Println("Длиннющая:\t", maxStrSlice)
}
