"""
Построение бинарного дерева
Option 8
Root = 8; height = 4, left_leaf = root+root/2, right_leaf = root^2
"""


def gen_bin_tree(height=2, root=8, left_leaf=lambda x: x + x / 2, right_leaf=lambda x: x ** 2) -> dict:

    """
    Функция создания бинарного дерева в виде словаря с использованием нерекурсивного метода.

    right_leaf(root: int) - функция для правой ветки (root ** 2 при целом root возвращает int),
    left_leaf(root: float) - функция для левой ветки (root + root / 2 при любом root возвращает float)

    Структура дерева:
        - При height = 0 функция возвращает только корень (root)
        - При height > 0 функция нерекурсивно строит дерево (левая и правая ветки):
            1. Каждый узел (находится внутри фигурных скобок '{}', представляет собой словарь) выглядит как
            {value: [left_tree, right_tree]}, нижние уровни представляют из себя списки в словаре:
             {value: [l_value, r_value]}
            2. Сначала выводится корень дерева, затем его левая ветка, для каждого значения
            левой ветки выводятся свои левые ветки, на нижнем уровне выводится левое и правое значения,
            правые ветки выводятся после вывода левых веток

    Аргументы:
        - height: высота дерева (максимальное количество узлов на пути от корневого узла до самого дальнего листового узла).
        Может принимать только натуральные значения
        - root: вершина дерева, может принимать положительные числа типа int и float
        - left_leaf=lambda x: x + x / 2 функция для вычисления левого потомка
        - right_leaf=lambda x: x ** 2 функция для вычисления правого потомка

    Возвращения:
        dict: Словарь, представляющий бинарное дерево, где каждый узел имеет структуру
              {value: [left_tree, right_tree]}
        str: Сообщение об ошибке в случае невалидных входных данных

    Пример:
    >>> gen_bin_tree(0, 8) # height = 0
        {8}
    >>> gen_bin_tree(1, 8) # height = 1
        {8: [12.0, 64]}
    >>> gen_bin_tree(2, 8) # height = 2
        {8: [{12.0: [18.0, 144.0]}, {64: [96.0, 4096]}]}
    """

    if type(root) != int and type(root) != float or type(height) != int:
        return 'Неверный тип данных'

    elif height < 0 or root < 0:
        return 'Высота и корень дерева не могут быть отрицательными'

    elif height == 0:
        return {root}

    else:

        tree = {root: []}
        check = [(tree[root], root, 1)]

        while len(check) > 0:

            res, value, level = check.pop(0)
            l_value = left_leaf(value)
            r_value = right_leaf(value)

            if level == height:

                res.append(l_value)
                res.append(r_value)

            elif level < height:

                left_tree, right_tree = {l_value: []}, {r_value: []}

                res.append(left_tree)
                res.append(right_tree)

                check.append((left_tree[l_value], l_value, level + 1))
                check.append((right_tree[r_value], r_value, level + 1))

            else:

                break

        return tree
