import math

# итерация 1
def integrate(f, a: float, b: float, *, n_iter: int=100000) -> float:
    '''
    Численное интегрирование функции методом левых прямоугольников на промежутке [a, b].

    Параметры:
    f (callable): Интегрируемая функция одного аргумента.
    a (float): Нижний предел интегрирования.
    b (float): Верхний предел интегрирования.
    n_iter (int): Количество итераций (разбиений интервала), по умолчанию 100000.

    Возвращения:
    float: Приближенное значение интеграла.

    Примеры реализации:
    >>> # 1. Простая тригонометрическая функция sin(x)
    >>> round(integrate(math.sin, 0, math.pi, n_iter=1000), 5)
    2.0

    >>> # 2. Полиномиальная функция второго порядка x²
    >>> round(integrate(lambda x: x**2, 0, 1, n_iter=1000), 5)
    0.33283
    '''


    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i*step) * step
    return acc


integrate(math.sin, 0, math.pi / 2, n_iter=1000)

