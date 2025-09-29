from lab2 import main   
import unittest
# import main


class TestGuessingGame(unittest.TestCase):

    def test_guess1(self): # загаданное число в середине диапазона
        self.assertEqual(main([1, 2, 3, 4, 5], 3), (2, 1))
        
    def test_guess2(self): # загаданное число в начале диапазона
        self.assertEqual(main([9, 10, 11, 12, 13], 9), (0, 2))
        
    def test_guess3(self): # большой диапазон
        self.assertEqual(main(list(range(1, 100)), 56), (55, 4)) 
        
    def test_guess4(self): # левая граница больше правой
        self.assertEqual(main([5, 4, 3, 2, 1], 5), None)
        
    def test_guess5(self): # наличие строкового типа данных
        self.assertEqual(main(['a', '2', 3, 4, 5], 4), (3, 2))
        
    def test_guess6(self): # наличие типа данных float
        self.assertEqual(main([1.1, 2.2, 3.3, 4.4, 5.5], 4), None)
        
    def test_guess7(self): # числа нет в диапазоне
        self.assertEqual(main([1, 2, 3, 4, 5], 6), None)


if __name__ == '__main__':
    unittest.main()
