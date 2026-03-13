import cython
from libc.math cimport sin, cos, exp

cdef extern from "math.h":
    double pow(double x, double y)

# 1. C-функция (только внутри Cython)

@cython.cdivision(True)
cdef double integrate_c_version(double (*f)(double), double a, double b, int n_iter):
    cdef double h = (b - a) / n_iter
    cdef double total = 0.0
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * h
        total += f(x)

    return total * h

# 2. Гибридные функции (быстрые, для конкретных функций)

cpdef double integrate_fast_sin(double a, double b, int n_iter=100000):
    return integrate_c_version(sin, a, b, n_iter)

cpdef double integrate_fast_cos(double a, double b, int n_iter=100000):
    return integrate_c_version(cos, a, b, n_iter)

cpdef double integrate_fast_exp(double a, double b, int n_iter=100000):
    return integrate_c_version(exp, a, b, n_iter)

cpdef double integrate_fast_pow2(double a, double b, int n_iter=100000):
    cdef double h = (b - a) / n_iter
    cdef double total = 0.0
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * h
        total += x * x

    return total * h

# 3. Универсальная, для любых функций Python)

def integrate_python_version(f, double a, double b, int n_iter=100000):
    cdef double h = (b - a) / n_iter
    cdef double total = 0.0
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * h
        total += f(x)

    return total * h


integrate = integrate_python_version
