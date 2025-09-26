from lab3 import gen_bin_tree
import unittest
# import main


class TestBinaryTree(unittest.TestCase):

    def binary_test1(self):
        self.assertEqual(gen_bin_tree([0, 1]), [1])


unittest.main()
