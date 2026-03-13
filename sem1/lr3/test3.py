from lab3 import gen_bin_tree
import unittest


class TestBinaryTree(unittest.TestCase):

    def test_binary1(self): # проверка построения дерева с height = 0
        self.assertEqual(gen_bin_tree(0, 3), [3])

    def test_binary2(self): # проверка построения дерева с height > 0
        self.assertEqual(gen_bin_tree(1, 10), [10, [15.0, 100]])

    def test_simple3(self): # проверка построения дерева с нецелым height
        self.assertEqual(gen_bin_tree(0.5, 2), 'Неверный тип данных')

    def test_simple4(self): # проверка построения дерева с отрицательным height
        self.assertEqual(gen_bin_tree(-1, 2), 'Высота и корень дерева не могут быть отрицательными')

    def test_simple5(self): # проверка построения дерева с отрицательным root
        self.assertEqual(gen_bin_tree(1, -2), 'Высота и корень дерева не могут быть отрицательными')

    def test_simple6(self): # проверка построения дерева с отрицательным root
        self.assertEqual(gen_bin_tree('a', 3), 'Неверный тип данных')

    def test_simple7(self): # проверка построения дерева с root, не являющегося числом
        self.assertEqual(gen_bin_tree(3, 'a'), 'Неверный тип данных')


if __name__ == '__main__':
    unittest.main()
