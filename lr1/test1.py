from lab1 import two_sum
import unittest
# import main


class TestMySolution(unittest.TestCase):

    def test_simple1(self): # проверка при хороших nums и target
        self.assertEqual(two_sum([3, 3], 6), [0, 1])
        
    def test_simple2(self): # проверка работы функции
        self.assertEqual(two_sum([4, 9, 2, 5], 7), [2, 3])
        
    def test_simple3(self): # проверка при большом списке
        self.assertEqual(two_sum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 3), [0, 1])
        
    def test_simple4(self): # проверка при наличии строки в nums
        self.assertEqual(two_sum([2, 'a', 4, 5], 7), 'Неверный тип данных')
        
    def test_simple5(self): # проверка при наличии типа данных float в nums
        self.assertEqual(two_sum([21.4, 7.6, 45, 3], 29.0), 'Неверный тип данных')
        
    def test_simple6(self): # проверка работы при отсутствии правильного решения
        self.assertEqual(two_sum([2, 3, 4, 5], 10), None)
        
    def test_simple7(self): # проверка при наличии отрицательных чисел в nums
        self.assertEqual(two_sum([-2, -3, -4, -5], -7), [0, 3])
        
    def test_simple8(self): # проверка при наличии отрицательных чисел и отсутствии правильного решения
        self.assertEqual(two_sum([-5.4, -4.6, -3, -2, 1], -10), 'Неверный тип данных')

if __name__ == '__main__':
    unittest.main()
