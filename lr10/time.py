from iteration1 import integrate
from iteration2 import integrate_async
from iteration3 import integrate_process

try:
    import pyximport
    pyximport.install(language_level=3)
    import cython_integrate

except Exception as e:
    print("Cython не загружен: {e}")


from iteration5 import integrate_processes_mp
import math
import time

if __name__ == "__main__":

    n_iter = 10_000_000

    print(f"Тест: ∫cos(x)dx от 0 до π")
    print(f"Итераций: {n_iter:,}")
    print("-" * 50)

    # 1. Базовая
    start = time.perf_counter()
    r1 = integrate(math.cos, 0.0, math.pi, n_iter=n_iter)
    t1 = time.perf_counter() - start

    # 2. Потоки
    start = time.perf_counter()
    r2 = integrate_async(math.cos, 0.0, math.pi, n_iter=n_iter)
    t2 = time.perf_counter() - start

    # 3. Процессы
    start = time.perf_counter()
    r3 = integrate_process(math.cos, 0.0, math.pi, n_iter=n_iter)
    t3 = time.perf_counter() - start

    # 4. Cython - пробуем разные варианты (разные виды функций)
    try:
        # Вариант 1
        start = time.perf_counter()
        r4 = cython_integrate.integrate_python_version(math.cos, 0.0, math.pi, n_iter)
        t4 = time.perf_counter() - start
        cython_ok = True
    except:
        try:
            # Вариант 2
            start = time.perf_counter()
            r4 = cython_integrate.integrate_cy(math.cos, 0.0, math.pi, n_iter)
            t4 = time.perf_counter() - start
            cython_ok = True
        except:
            try:
                # Вариант 3
                start = time.perf_counter()
                r4 = cython_integrate.integrate(math.cos, 0.0, math.pi, n_iter)
                t4 = time.perf_counter() - start
                cython_ok = True
            except Exception as e:
                print(f"Cython ошибка: {e}")
                cython_ok = False
                r4 = 0
                t4 = 0

    # 5. Мультипроцессинг
    start = time.perf_counter()
    r5 = integrate_processes_mp(math.cos, 0.0, math.pi, n_jobs=2, n_iter=n_iter)
    t5 = time.perf_counter() - start

    print(f"Integrate_1:           {t1:.4f} сек | {r1:.5f}")
    print(f"Integrate_2_async:     {t2:.4f} сек | {r2:.5f}")
    print(f"Integrate_3_process:   {t3:.4f} сек | {r3:.5f}")
    if cython_ok:
        print(f"Cython:                {t4:.4f} сек | {r4:.5f}")
    print(f"Integrate_5_mp:        {t5:.4f} сек | {r5:.5f}")
