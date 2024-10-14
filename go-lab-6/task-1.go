package main

import (
	f "fmt"
	m "math"
	r "math/rand"
	s "sync"
	t "time"
)

// 1

func Factorial(n int) int {
	if n == 0 {
		return 1
	}
	if n < 0 {
		return 0
	}
	return n * Factorial(n-1)
}

func Random() int {
	return r.Intn(10)
}

func Sum(nums []int) int {
	sum := 0
	for _, num := range nums {
		sum += num
	}
	return sum
}

func Task1() {
	f.Println("\n>> Задача 1")

	go f.Println("Факториал числа:", Factorial(4))
	t.Sleep(300 * t.Millisecond)

	go f.Println("Случайные числа:", Random(), Random(), Random())
	t.Sleep(300 * t.Millisecond)

	go f.Println("Сумма чисел:\t", Sum([]int{1, 20, 3, 4, 5}))
	t.Sleep(300 * t.Millisecond)
}

// 2

func Fibonacci(n int) int {
	if n == 0 {
		return 0
	}
	if n == 1 {
		return 1
	}
	return Fibonacci(n-1) + Fibonacci(n-2)
}

func FibonacciSequence(n int) []int {
	var fibs []int
	for i := 0; i < n; i++ {
		fibs = append(fibs, Fibonacci(i))
	}
	return fibs
}

func fillChannel(ch chan int) {
	for _, num := range FibonacciSequence(10) {
		ch <- num
	}
	close(ch)
}

func printChannel(ch chan int) {
	for num := range ch {
		f.Println(num)
	}

}

func Task2() {
	f.Println("\n>> Задача 2")

	ch := make(chan int)

	go fillChannel(ch)
	t.Sleep(300 * t.Millisecond)

	go printChannel(ch)
	t.Sleep(300 * t.Millisecond)

}

// 3

func fillChannelWithRandomNumbers(ch chan int, n int) {
	for i := 0; i < n; i++ {
		ch <- r.Intn(10)
		// t.Sleep(100 * t.Millisecond)
	}
}

func checkChannelsParity(numCh chan int, outputCh chan string) {
	for num := range numCh {
		if num%2 == 0 {
			outputCh <- f.Sprint(num, " - чётное")
		} else {
			outputCh <- f.Sprint(num, " - нечётное")
		}
		// t.Sleep(100 * t.Millisecond)
	}

}

func Task3() {
	f.Println("\n>> Задача 3")

	numbersChannel := make(chan int)
	parityChannel := make(chan string)

	numberOfNumbers := 4

	go fillChannelWithRandomNumbers(numbersChannel, numberOfNumbers)
	// for num := range numbersChannel {
	// 	f.Println(num)
	// }

	go checkChannelsParity(numbersChannel, parityChannel)
	// for par := range parityChannel {
	// 	f.Println(par)
	// }

	for i := 0; i < numberOfNumbers; i++ {
		select {
		case num := <-numbersChannel:
			f.Println("Число:", num)
		case message := <-parityChannel:
			f.Println(message)
		}
	}
}

// 4

func Task4() {
	f.Println("\n>> Задача 4")

	var counter int
	wg := new(s.WaitGroup)
	mu := new(s.Mutex)

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			// вызывается после завершения работы горутины
			// не смотря на ошибки и прочее
			mu.Lock()
			counter++
			mu.Unlock()
		}()
	}

	wg.Wait()
	f.Println(counter)
}

// 5

type CalcRequest struct {
	firstNum  float64
	operation string
	secondNum float64
	result    chan float64
}

func calculator(requests chan CalcRequest) {
	for req := range requests {
		var res float64
		switch req.operation {
		case "+":
			res = req.firstNum + req.secondNum
		case "-":
			res = req.firstNum - req.secondNum
		case "*":
			res = req.firstNum * req.secondNum
		case "/":
			if req.secondNum != 0 {
				res = req.firstNum / req.secondNum
			} else {
				f.Println("Деление на ноль не допускается")
				req.result <- m.Inf(1)
				continue
			}
		default:
			f.Println("Операция не предусмотрена")
			req.result <- m.Inf(1)
			continue
		}
		req.result <- res
	}
}

func Task5() {
	f.Println("\n>> Задача 5")

	requests := make(chan CalcRequest)
	results := make(chan float64)

	requestList := []CalcRequest{
		{10.5, "+", 10.5, results},
		{10.5, "-", 10.5, results},
		{10.5, "*", 10.5, results},
		{10.5, "/", 10.5, results},
		{10, "/", 0, results},
		{10, "%", 10, results},
		{20, "+", 20, results},
		{20, "-", 20, results},
		{20, "*", 20, results},
		{20, "/", 20, results},
	}

	go calculator(requests)

	for _, req := range requestList {
		go func(req CalcRequest) {
			requests <- req
			res := <-req.result
			if res == m.Inf(1) {
			} else {
				f.Printf("%f %s %f = %f\n", req.firstNum, req.operation, req.secondNum, res)
			}
		}(req)
	}
	t.Sleep(t.Millisecond * 100)

	close(requests)
	close(results)
}

// 6

func worker(_ int, jobs <-chan string, results chan<- string) {
	for j := range jobs {
		t.Sleep(t.Millisecond * 500)
		reversedRow := reverseRow(j)
		results <- reversedRow
	}
}

func reverseRow(str string) string {

	var strReverse string = ""

	for i := len(str) - 1; i >= 0; i-- {
		strReverse = strReverse + string(str[i])
	}

	return strReverse
}

func Task6() {
	f.Println("\n>> Задача 6")

	f.Printf("Введите количество воркеров: ")
	var workersCount int
	f.Scan(&workersCount)

	jobList := []string{"worker", "GO", "lab", "calculator", "testing", "python"}
	jobsCount := len(jobList)

	jobs := make(chan string, jobsCount)
	results := make(chan string, jobsCount)

	for w := 1; w < workersCount+1; w++ {
		go worker(w, jobs, results)
	}

	for _, job := range jobList {
		jobs <- job
	}
	close(jobs)

	for i := 0; i < jobsCount; i++ {
		f.Println(<-results)
	}

}

//

func main() {
	Task1()
	Task2()
	Task3()
	Task4()
	Task5()
	Task6()
}
