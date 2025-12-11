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


# итерация 2
def integrate_async(f, a: float, b: float, *, n_jobs: int = 2, n_iter: int = 1000) -> float:
    '''
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием ThreadPoolExecutor (потоков).

    Распараллеливает вычисления, разделяя отрезок [a, b] на n_jobs
    подынтервалов. Каждый поток вычисляет интеграл на своем подынтервале
    с помощью функции integrate(), затем результаты суммируются.

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
        >>> round(integrate_async(math.log2, 1, 2, n_iter=10000), 5)
        Работник 0, границы: 1.0, 1.5
        Работник 1, границы: 1.5, 2.0
        0.55725

        >>> integrate_async(math.sin, 0, math.pi, n_jobs=4, n_iter=10000)
        Работник 0, границы: 0.0, 0.7853981633974483
        Работник 1, границы: 0.7853981633974483, 1.5707963267948966
        Работник 2, границы: 1.5707963267948966, 2.356194490192345
        Работник 3, границы: 2.356194490192345, 3.141592653589793
        2.000000000000001
    '''

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    step = (b - a) / n_jobs
    for i in range(n_jobs):
        print(f"Работник {i}, границы: {a + i * step}, {a + (i + 1) * step}")

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]

    return sum(list(f.result() for f in ftres.as_completed(fs)))
