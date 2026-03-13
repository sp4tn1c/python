import timeit
import matplotlib.pyplot as plt
import random


# Рекурсивная версия (возвращает список)
def left_leaf(root: float) -> float:
    return root + root / 2


def right_leaf(root: int) -> int:
    return root ** 2


def gen_bin_tree_recursive(height: int, root: float) -> list:

    """
    Функция создания бинарного дерева с помощью рекурсии.

    right_leaf(root: int) - функция для правой ветки (root ** 2 при целом root возвращает int),
    left_leaf(root: float) - функция для левой ветки (root + root / 2 при любом root возвращает float)

    Структура дерева:
        - При height = 0 функция возвращает только корень (root)
        - При height > 0 функция рекурсивно строит дерево (левая и правая ветки):
            1. Каждый узел (находится внутри квадратных скобок '[]') представляется как
            [значение, левая_ветка, правая_ветка]
            2. Сначала выводится корень дерева, затем его левая ветка, для каждого значения
            левой ветки выводятся свои левые ветки, на нижнем уровне выводится левое и правое значения,
            правые ветки выводятся после вывода левых веток

    Аргументы:
        - height: высота дерева (максимальное количество узлов на пути от корневого узла до самого дальнего листового узла).
        Может принимать только натуральные значения
        - root: вершина дерева, может принимать положительные числа типа int и float

    Возвращения:
        Бинарное дерево в виде списка списков, каждый из которых является поддеревом основного бинарного дерева

    Пример:
        >> gen_bin_tree(0, 8) # height = 0
        [8]
        >> gen_bin_tree(1, 8) # height = 1
        [8, [12.0, 64]]
        >> gen_bin_tree(2, 8) # height = 2
        [8, [12.0, [18.0, 144.0], 64, [96.0, 4096]]]

    В последнем примере root=8, его левая ветвь: 12.0, [18.0, 144.0], его правая ветвь: 64, [96.0, 4096]
    """

    if type(root) != int and type(root) != float or type(height) != int:
        return 'Неверный тип данных'

    elif height < 0 or root < 0:
        return 'Высота и корень дерева не могут быть отрицательными'

    elif height == 0:
        return [root]

    else:

        return [root] + [
            gen_bin_tree_recursive(height - 1, left_leaf(root)) + gen_bin_tree_recursive(height - 1, right_leaf(root))]


# Нерекурсивная версия (возвращает список для совместимости)
def gen_bin_tree_iterative(height=2, root=8, left_leaf=lambda x: x + x / 2, right_leaf=lambda x: x ** 2) -> dict:
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
        >> gen_bin_tree(0, 8) # height = 0
            {8}
        >> gen_bin_tree(1, 8) # height = 1
            {8: [12.0, 64]}
        >> gen_bin_tree(2, 8) # height = 2
            {8: [{12.0: [18.0, 144.0]}, {64: [96.0, 4096]}]}
        """

    if type(root) != int and type(root) != float or type(height) != int:
        return 'Неверный тип данных'

    elif height < 0 or root < 0:
        return 'Высота и корень дерева не могут быть отрицательными'

    elif height == 0:
        return {root}

    else:

        # Преобразуем словарное представление в списковое для совместимости

        tree_dict = {root: []}
        stack = [(tree_dict[root], root, 1)]

        while len(stack) > 0:
            res, value, level = stack.pop(0)
            l_value = left_leaf(value)
            r_value = right_leaf(value)

            if level == height:

                res.append(l_value)
                res.append(r_value)

            elif level < height:

                left_tree = {l_value: []}
                right_tree = {r_value: []}
                res.append(left_tree)
                res.append(right_tree)
                stack.append((left_tree[l_value], l_value, level + 1))
                stack.append((right_tree[r_value], r_value, level + 1))

            else:

                break

        def to_list(d):

            """
            Рекурсивно преобразует словарное представление дерева в списковое

            Аргументы:
                dict: Словарь для преобразования в список (d)

            Возвращает:
                list: Дерево в списковом формате
            """

            if type(d) == dict:
                for key, value in d.items():
                    return [key] + to_list(value)
            elif type(d) == list:
                result = []
                for item in d:
                    if type(d) == list:
                        result.extend(to_list(item))
                    else:
                        result.append(item)
                return result
            else:
                return [d]

        return to_list(tree_dict)


def benchmark(func, n, repeat=5):
    """
        Измеряет минимальное время выполнения функции для заданной высоты дерева.

        Аргументы:
            func (callable): Функция для тестирования (gen_bin_tree_recursive или gen_bin_tree_iterative)
            n (int): Высота дерева для тестирования
            repeat (int): Количество повторных замеров времени

        Возвращает:
            float: Минимальное время выполнения в секундах
        """

    times = timeit.repeat(lambda: func(n, 8), number=1, repeat=repeat)
    return min(times)


def main():
    """
        Основная функция для сравнения производительности рекурсивного и итеративного методов.

        Создает график зависимости времени выполнения от высоты дерева
        для обоих методов построения бинарных деревьев.
    """

    random.seed(42)
    test_data = list(range(1, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:

        res_recursive.append(benchmark(gen_bin_tree_recursive, n, repeat=3))
        res_iterative.append(benchmark(gen_bin_tree_iterative, n, repeat=3))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
