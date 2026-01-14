import multiprocessing as mp
from iteration1 import integrate


def worker(f, a_seg, b_seg, n_seg, result_queue, idx):
    # вспомогательная функция для описание отдельного процесса
    result = integrate(f, a_seg, b_seg, n_iter=n_seg)
    result_queue.put((idx, result))


def integrate_processes_mp(f, a, b, *, n_jobs=2, n_iter=10000):
    '''
    """
    Вычисляет определенный интеграл функции f на отрезке [a, b]
    с использованием многопроцессорности (multiprocessing), так как
    не получилось установить noGIL из-за версии.

    Аргументы:
    - f: функция для интегрирования (math.cos, math.sin и т.д.)
    - a, b: пределы интегрирования (a < b)
    - n_jobs: количество процессов (по умолчанию 2)
    - n_iter: общее число итераций (по умолчанию 100000)

    Возвращения: приближенное значение интеграла

    Пример:
    >>> integrate_processes_mp(math.cos, 0, math.pi, n_jobs=4)
    0.0003141592653589793

    '''
    if n_jobs <= 0:
        n_jobs = 1

    if n_iter < n_jobs:
        n_iter = n_jobs

    result_queue = mp.Queue()
    processes = []

    step = (b - a) / n_jobs
    seg_iter = n_iter // n_jobs

    for i in range(n_jobs):
        a_seg = a + i * step
        b_seg = a + (i + 1) * step

        p = mp.Process(
            target=worker,
            args=(f, a_seg, b_seg, seg_iter, result_queue, i)
        )
        processes.append(p)
        p.start()

    results = [0.0] * n_jobs
    for _ in range(n_jobs):
        idx, result = result_queue.get()
        results[idx] = result

    for p in processes:
        p.join()
        p.close()

    return sum(results)
