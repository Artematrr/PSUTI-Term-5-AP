import random
import time
import threading
import concurrent.futures
from queue import Queue

# 1


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def random_numbers():
    return [random.randint(1, 10) for _ in range(3)]


def sum_of_numbers(nums):
    return sum(nums)


def task1():
    print("\n>> Задача 1")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(lambda: print(f"Факториал числа: {factorial(4)}"))
        time.sleep(0.3)

        executor.submit(lambda: print(f"Случайные числа: {random_numbers()}"))
        time.sleep(0.3)

        executor.submit(lambda: print(
            f"Сумма чисел: {sum_of_numbers([1, 20, 3, 4, 5])}"))
        time.sleep(0.3)

# 2


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_sequence(n):
    return [fibonacci(i) for i in range(n)]


def fill_queue(q):
    for num in fibonacci_sequence(10):
        q.put(num)
    q.put(None)  # сигнал завершения


def print_queue(q):
    while True:
        num = q.get()
        if num is None:
            break
        print(num)


def task2():
    print("\n>> Задача 2")

    q = Queue()

    threading.Thread(target=fill_queue, args=(q,)).start()
    time.sleep(0.3)

    threading.Thread(target=print_queue, args=(q,)).start()
    time.sleep(0.3)

# 3


def check_parity(num):
    return f"{num} - чётное" if num % 2 == 0 else f"{num} - нечётное"


def task3():
    print("\n>> Задача 3")

    def generate_numbers(num_q):
        for _ in range(4):
            num_q.put(random.randint(1, 10))
        num_q.put(None)  # сигнал завершения

    def check_parity_queue(num_q, parity_q):
        while True:
            num = num_q.get()
            if num is None:
                parity_q.put(None)  # сигнал завершения для паритета
                break
            parity_q.put(check_parity(num))

    num_q = Queue()
    parity_q = Queue()

    threading.Thread(target=generate_numbers, args=(num_q,)).start()
    threading.Thread(target=check_parity_queue, args=(num_q, parity_q)).start()

    while True:
        if not num_q.empty():
            num = num_q.get()
            if num is None:
                break
            print(f"Число: {num}")

        if not parity_q.empty():
            parity_msg = parity_q.get()
            if parity_msg is None:
                break
            print(parity_msg)

        time.sleep(0.5)


# 4


def increment_counter():
    global counter
    with counter_lock:
        counter += 1


def task4():
    print("\n>> Задача 4")

    threads = []
    for _ in range(1000):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(counter)


counter = 0
counter_lock = threading.Lock()

# 5


def calculator_worker(requests):
    while True:
        req = requests.get()
        if req is None:
            break
        num1, op, num2, result = req
        if op == '+':
            result.put(num1 + num2)
        elif op == '-':
            result.put(num1 - num2)
        elif op == '*':
            result.put(num1 * num2)
        elif op == '/':
            if num2 != 0:
                result.put(num1 / num2)
            else:
                result.put(float('nan'))
                print(f"Деление на ноль!")
        else:
            result.put(float('nan'))
            print(f"Неизвестная операция: {op}")


def task5():
    print("\n>> Задача 5")

    requests = Queue()
    results = Queue()

    threading.Thread(target=calculator_worker, args=(requests,)).start()

    operations = [
        (10.5, '+', 10.5),
        (10.5, '-', 10.5),
        (10.5, '*', 10.5),
        (10.5, '/', 10.5),
        (10, '/', 0),
        (10, '%', 10)
    ]

    for num1, op, num2 in operations:
        req = (num1, op, num2, results)
        requests.put(req)
        result = results.get()
        if result != float('nan'):
            print(f"{num1} {op} {num2} = {result}")

    requests.put(None)

# 6


def worker_task(jobs, results):
    while True:
        job = jobs.get()
        if job is None:
            break
        time.sleep(0.2)
        results.put(job[::-1])
        jobs.task_done()


def result_printer(results, jobs):
    while True:
        result = results.get()
        print(result)
        if jobs.empty() and results.empty():
            break


def task6():
    print("\n>> Задача 6")

    workers_count = int(input("Введите количество воркеров: "))
    job_list = ["worker", "GO", "lab", "calculator", "testing", "python"]

    jobs = Queue()
    results = Queue()

    for _ in range(workers_count):
        threading.Thread(target=worker_task, args=(jobs, results)).start()

    # Сразу стараемся вывести резалт каждого воркера
    threading.Thread(target=result_printer, args=(
        results, jobs), daemon=True).start()

    for job in job_list:
        jobs.put(job)

    for _ in range(workers_count):
        jobs.put(None)  # тож сигнал для завершения воркеров

    jobs.join()


if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
