import os
import sys
import unittest
import math

# Добавляем текущую папку в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from iteration1 import integrate
from iteration2 import integrate_async
from iteration3 import integrate_process

try:
    import pyximport
    pyximport.install(language_level=3)
    import cython_integrate

except Exception as e:
    print("Cython не загружен: {e}")


from iteration5 import worker, integrate_processes_mp


class TestIntegrate_first_iteration(unittest.TestCase):
    def test_exp(self):
        result = integrate(math.exp, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 4.66843, delta=0.001)

    def test_sin(self):
        result = integrate(math.sin, 0, math.pi / 2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)

class TestIntegrate_second_iteration(unittest.TestCase):
    def test_log2(self):
        result = integrate_async(math.exp, 1, 2, n_iter=1000 , n_jobs=2)
        self.assertAlmostEqual(result, 4.66843, delta=0.001)

    def test_sin(self):
        result = integrate_async(math.sin, 0, math.pi/2, n_iter=1000)
        self.assertAlmostEqual(result, 1, delta=0.001)

class TestIntegrate_third_iteration(unittest.TestCase):
    def test_exp(self):
        result = integrate_process(math.exp, 1, 2, n_iter=1000 , n_jobs=2)
        self.assertAlmostEqual(result, 4.66843, delta=0.001)

    def test_sin(self):
        result = integrate_process(math.sin, 0, math.pi/2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)

class TestIntegrate_cython_iteration(unittest.TestCase):
    def test_exp(self):
        result = cython_integrate.integrate_python_version(math.exp, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 4.66843, delta=0.001)

    def test_sin(self):
        result = cython_integrate.integrate_python_version(math.sin, 0, math.pi/2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)

class TestIntegrate_noGIL_for_5st_task(unittest.TestCase):
    def test_exp(self):
        result = integrate_processes_mp(math.exp, 1, 2, n_jobs=2, n_iter=1000)
        self.assertAlmostEqual(result, 4.66843, delta=0.001)

    def test_sin(self):
        result = integrate_processes_mp(math.sin, 0, math.pi/2, n_jobs= 2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)


