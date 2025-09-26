'''
Построение бинарного дерева
Option 8
Root = 8; height = 4, left_leaf = root+root/2, right_leaf = root^2
'''

def left_leaf(root:int): # левая ветка бинарного дерева
    return root + root / 2


def right_leaf(root:int) -> int: # левая ветка бинарного дерева
    return root ** 2


def gen_bin_tree(height:int, root) -> list: # бинарное дерево
    '''
    Функция создания бинарного дерева с помощью рекурсии.
    '''
    if height == 0: # если высота дерва равна 0, то возвращаем вершину дерева
        return [root]
    return [root] + [gen_bin_tree(height - 1, left_leaf(root)) + gen_bin_tree(height - 1, right_leaf(root))]


if __name__ == '__main__':
    gen_bin_tree(4, 8)



