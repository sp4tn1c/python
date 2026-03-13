import math
import concurrent.futures as ftres
from functools import partial

# итерация 1
def integrate(f, a: float, b: float, *, n_iter: int=100000) -> float:
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i*step) * step
    return acc

# Определяем именованную функцию для полинома
def square_function(x: float) -> float:
    """Функция x²."""
    return x * x

# итерация 3
def integrate_process(f, a: float, b: float, *, n_jobs: int = 2, n_iter: int = 1000) -> float:
    '''
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием ProcessPoolExecutor (процессов).

    Параметры:

    f : функция
        Функция одного аргумента, интеграл которой вычисляется.
        Должна быть потокобезопасной.
        Примеры: math.sin, math.log2, lambda x: x**2

    a : float
        Нижний предел интегрирования.
        Должно выполняться: a < b.
        Пример: 0.0, 1.0

    b : float
        Верхний предел интегрирования.
        Должно выполняться: a < b.
        Пример: 1.0, 2.0, math.pi

    n_jobs : int
        Количество потоков для параллельного выполнения.
        Каждому потоку выделяется подынтервал размера (b - a) / n_jobs.
        Примеры: 2, 4, 8

    n_iter : int, optional
        Общее количество итераций для численного интегрирования,
        по умолчанию 1000.
        Распределяется между потоками: каждый поток выполняет
        n_iter // n_jobs итераций.

    Возвращения:

    float
        Приближенное значение интеграла ∫[a, b] f(x) dx.

    Примеры реализации:
        >>> # 1. Простая тригонометрическая функция log2(x)
        >>> round(integrate_process(math.log2, 1, 2, n_jobs=4, n_iter=10000), 5)
        Распределение работы между 4 процессами:
        Процесс 0: отрезок [1.0000, 1.2500], итераций: 2500
        Процесс 1: отрезок [1.2500, 1.5000], итераций: 2500
        Процесс 2: отрезок [1.5000, 1.7500], итераций: 2500
        Процесс 3: отрезок [1.7500, 2.0000], итераций: 2500
        0.55725

        >>> # 2. Полиномиальная функция второго порядка x²
        >>> round(integrate_process(square_function, 0, 1, n_jobs=2, n_iter=1000), 5)
        Распределение работы между 2 процессами:
        Процесс 0: отрезок [0.0000, 0.5000], итераций: 500
        Процесс 1: отрезок [0.5000, 1.0000], итераций: 500
        0.33283

    '''
    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)

    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    print(f"Распределение работы между {n_jobs} процессами:")
    for i in range(n_jobs):
        a_i = a + i * step
        b_i = a + (i + 1) * step
        print(f"Процесс {i}: отрезок [{a_i:.4f}, {b_i:.4f}], "f"итераций: {n_iter // n_jobs}")


    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    results = [future.result() for future in ftres.as_completed(fs)]

    return sum(results)


