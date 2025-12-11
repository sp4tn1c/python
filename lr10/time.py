from iteration1 import integrate
from iteration2 import integrate_async
from iteration3 import integrate_process, square_function
import math
import time


def benchmark_comparison():
    """Сравнение производительности всех трех итераций."""

    n_iter = 1000000  # 1 миллион итераций

    # Тест 1: Простая функция sin(x)
    print("\n" + "=" * 60)
    print("ПРОСТАЯ ФУНКЦИЯ: sin(x) от 0 до π")
    print("=" * 60)
    print(f"Ожидаемый результат: 2.000000")
    print(f"Количество итераций: {n_iter:,}")
    print("-" * 60)

    # 1. Базовая версия
    start = time.perf_counter()
    result_base = integrate(math.sin, 0, math.pi, n_iter=n_iter)
    time_base = time.perf_counter() - start
    print(f"\n1. Без потоков и процессов:")
    print(f"   Время: {time_base:.5f} сек")
    print(f"   Результат: {result_base:.6f}")

    # 2. Многопоточная версия
    print(f"\n2. Потоки")
    for n_jobs in [2, 4, 6, 8]:
        start = time.perf_counter()
        result = integrate_async(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
        elapsed = time.perf_counter() - start
        print(f"   {n_jobs} потока: {elapsed:.5f} сек, результат: {result:.6f}")

    # 3. Многопроцессная версия
    print(f"\n3. Процессы")
    for n_jobs in [2, 4, 6, 8]:
        start = time.perf_counter()
        result = integrate_process(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
        elapsed = time.perf_counter() - start
        print(f"   {n_jobs} процесса: {elapsed:.5f} сек, результат: {result:.6f}")

    # Тест 2: Полиномиальная функция x²
    print("\n" + "=" * 60)
    print("ПОЛИНОМИАЛЬНАЯ ФУНКЦИЯ: x² от 0 до 1")
    print("=" * 60)
    print(f"Ожидаемый результат: 0.333333")
    print(f"Количество итераций: {n_iter:,}")
    print("-" * 60)

    # 1. Базовая версия
    start = time.perf_counter()
    result_base = integrate(lambda x: x ** 2, 0, 1, n_iter=n_iter)
    time_base = time.perf_counter() - start
    print(f"\n1. Без потоков и процессов:")
    print(f"   Время: {time_base:.5f} сек")
    print(f"   Результат: {result_base:.6f}")

    # 2. Многопоточная версия
    print(f"\n2. Потоки")
    for n_jobs in [2, 4, 6, 8]:
        start = time.perf_counter()
        result = integrate_async(lambda x: x ** 2, 0, 1, n_jobs=n_jobs, n_iter=n_iter)
        elapsed = time.perf_counter() - start
        print(f"   {n_jobs} потока: {elapsed:.5f} сек, результат: {result:.6f}")

    # 3. Многопроцессная версия (используем глобальную функцию)
    print(f"\n3. Процессы")
    for n_jobs in [2, 4, 6, 8]:
        start = time.perf_counter()
        result = integrate_process(square_function, 0, 1, n_jobs=n_jobs, n_iter=n_iter)
        elapsed = time.perf_counter() - start
        print(f"   {n_jobs} процесса: {elapsed:.5f} сек, результат: {result:.6f}")


if __name__ == '__main__':
    benchmark_comparison()
