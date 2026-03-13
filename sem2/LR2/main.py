"""
ЛАБОРАТОРНАЯ РАБОТА 2: "Основы NumPy: массивы и векторные операции"
"""

import os
from typing import Union, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. СОЗДАНИЕ И ОБРАБОТКА МАССИВОВ
# ============================================================

def create_vector() -> np.ndarray:
    """Создать одномерный массив целых чисел от 0 до 9 включительно.

    Returns:
        np.ndarray: Массив shape=(10,) с числами [0, 1, ..., 9].

    Examples:
        >>> v = create_vector()
        >>> v.shape
        (10,)
    """
    return np.arange(10)


def create_matrix() -> np.ndarray:
    """Создать матрицу 5×5 со случайными числами из распределения [0, 1).

    Returns:
        np.ndarray: Матрица shape=(5, 5) со значениями в диапазоне [0, 1).

    Examples:
        >>> m = create_matrix()
        >>> m.shape
        (5, 5)
    """
    return np.random.rand(5, 5)


def reshape_vector(vec: np.ndarray) -> np.ndarray:
    """Преобразовать одномерный массив формы (10,) в матрицу формы (2, 5).

    Args:
        vec (np.ndarray): Входной массив формы (10,).

    Returns:
        np.ndarray: Массив формы (2, 5), заполненный построчно.

    Raises:
        ValueError: Если входной массив не имеет формы (10,).

    Examples:
        >>> v = np.arange(10)
        >>> reshape_vector(v).shape
        (2, 5)
    """
    return vec.reshape(2, 5)


def transpose_matrix(mat: np.ndarray) -> np.ndarray:
    """Выполнить транспонирование матрицы.

    Args:
        mat (np.ndarray): Входная матрица произвольной формы.

    Returns:
        np.ndarray: Транспонированная матрица.

    Examples:
        >>> m = np.array([[1, 2], [3, 4]])
        >>> transpose_matrix(m)
        array([[1, 3],
               [2, 4]])
    """
    return mat.T


# ============================================================
# 2. ВЕКТОРНЫЕ ОПЕРАЦИИ
# ============================================================

def vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Выполнить поэлементное сложение двух векторов одинаковой длины.

    Args:
        a (np.ndarray): Первый вектор.
        b (np.ndarray): Второй вектор той же формы.

    Returns:
        np.ndarray: Результат поэлементного сложения.

    Raises:
        ValueError: Если формы массивов не совпадают.

    Examples:
        >>> vector_add(np.array([1, 2]), np.array([3, 4]))
        array([4, 6])
    """
    return a + b


def scalar_multiply(vec: np.ndarray, scalar: Union[int, float]) -> np.ndarray:
    """Умножить вектор на скалярное значение.

    Args:
        vec (np.ndarray): Входной вектор.
        scalar (Union[int, float]): Скалярный множитель.

    Returns:
        np.ndarray: Вектор, умноженный на скаляр.

    Examples:
        >>> scalar_multiply(np.array([1, 2, 3]), 2)
        array([2, 4, 6])
    """
    return vec * scalar


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Выполнить поэлементное умножение двух массивов.

    Args:
        a (np.ndarray): Первый массив.
        b (np.ndarray): Второй массив той же формы.

    Returns:
        np.ndarray: Результат поэлементного умножения.

    Raises:
        ValueError: Если формы массивов не совпадают.

    Examples:
        >>> elementwise_multiply(np.array([1, 2, 3]), np.array([4, 5, 6]))
        array([ 4, 10, 18])
    """
    return a * b


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Вычислить скалярное произведение двух векторов.

    Args:
        a (np.ndarray): Первый вектор.
        b (np.ndarray): Второй вектор.

    Returns:
        float: Скалярное произведение.

    Raises:
        ValueError: Если векторы не одномерны или имеют разную длину.

    Examples:
        >>> dot_product(np.array([1, 2, 3]), np.array([4, 5, 6]))
        32
    """
    return float(np.dot(a, b))


# ============================================================
# 3. МАТРИЧНЫЕ ОПЕРАЦИИ
# ============================================================

def matrix_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Выполнить матричное умножение двух массивов.

    Args:
        a (np.ndarray): Левая матрица формы (m, n).
        b (np.ndarray): Правая матрица формы (n, p).

    Returns:
        np.ndarray: Результат умножения формы (m, p).

    Raises:
        ValueError: Если размеры матриц несовместимы для умножения.

    Examples:
        >>> A = np.array([[1, 2], [3, 4]])
        >>> B = np.array([[2, 0], [1, 2]])
        >>> matrix_multiply(A, B)
        array([[ 4,  4],
               [10,  8]])
    """
    return a @ b


def matrix_determinant(a: np.ndarray) -> float:
    """Вычислить определитель квадратной матрицы.

    Args:
        a (np.ndarray): Квадратная матрица формы (n, n).

    Returns:
        float: Значение определителя.

    Raises:
        ValueError: Если матрица не квадратная.

    Examples:
        >>> matrix_determinant(np.array([[1, 2], [3, 4]]))
        -2.0
    """
    return float(np.linalg.det(a))


def matrix_inverse(a: np.ndarray) -> np.ndarray:
    """Вычислить обратную матрицу.

    Args:
        a (np.ndarray): Квадратная невырожденная матрица.

    Returns:
        np.ndarray: Обратная матрица.

    Raises:
        np.linalg.LinAlgError: Если матрица вырожденная.
        ValueError: Если матрица не квадратная.

    Examples:
        >>> A = np.array([[1, 2], [3, 4]])
        >>> invA = matrix_inverse(A)
        >>> np.allclose(A @ invA, np.eye(2))
        True
    """
    return np.linalg.inv(a)


def solve_linear_system(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Решить систему линейных уравнений Ax = b.

    Args:
        a (np.ndarray): Матрица коэффициентов формы (n, n).
        b (np.ndarray): Вектор свободных членов формы (n,).

    Returns:
        np.ndarray: Вектор решения x.

    Raises:
        np.linalg.LinAlgError: Если матрица A вырождена.
        ValueError: Если матрица A не квадратная.

    Examples:
        >>> A = np.array([[2, 1], [1, 3]])
        >>> b = np.array([1, 2])
        >>> x = solve_linear_system(A, b)
        >>> np.allclose(A @ x, b)
        True
    """
    return np.linalg.solve(a, b)


# ============================================================
# 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================

def load_dataset(path: str = "data/students_scores.csv") -> np.ndarray:
    """Загрузить данные из CSV-файла и вернуть как NumPy-массив.

    Args:
        path (str): Путь к файлу в формате CSV.

    Returns:
        np.ndarray: Двумерный массив с данными.

    Raises:
        FileNotFoundError: Если файл не найден.
        pd.errors.EmptyDataError: Если файл пуст.

    Examples:
        >>> data = load_dataset("data/students_scores.csv")  # doctest: +SKIP
        >>> data.shape[1]
        3
    """
    return pd.read_csv(path).to_numpy()


def statistical_analysis(data: np.ndarray) -> Dict[str, float]:
    """Выполнить статистический анализ одномерного массива данных.

    Args:
        data (np.ndarray): Одномерный массив числовых данных.

    Returns:
        Dict[str, float]: Словарь со статистическими показателями.

    Examples:
        >>> data = np.array([10, 20, 30])
        >>> result = statistical_analysis(data)
        >>> round(result["mean"], 1)
        20.0
    """
    return {
        "mean": float(np.mean(data)),
        "median": float(np.median(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "percentile_25": float(np.percentile(data, 25)),
        "percentile_75": float(np.percentile(data, 75)),
    }


def normalize_data(data: np.ndarray) -> np.ndarray:
    """Выполнить Min-Max нормализацию данных к диапазону [0, 1].

    Args:
        data (np.ndarray): Входной массив числовых данных.

    Returns:
        np.ndarray: Нормализованный массив в диапазоне [0, 1].

    Raises:
        ValueError: Если все элементы массива одинаковы.

    Examples:
        >>> normalize_data(np.array([0, 5, 10]))
        array([0. , 0.5, 1. ])
    """
    min_val = np.min(data)
    max_val = np.max(data)

    return (data - min_val) / (max_val - min_val)


# ============================================================
# 5. ВИЗУАЛИЗАЦИЯ
# ============================================================

def plot_histogram(
    data: np.ndarray,
    bins: int = 10,
    output_path: str = "plots/histogram.png"
) -> None:
    """Построить и сохранить гистограмму распределения данных.

    Args:
        data (np.ndarray): Одномерный массив данных для визуализации.
        bins (int): Количество интервалов гистограммы (по умолчанию 10).
        output_path (str): Путь для сохранения изображения.

    Returns:
        None

    Raises:
        ValueError: Если data не является одномерным массивом.
        OSError: Если не удается сохранить файл.

    Examples:
        >>> data = np.array([1, 2, 3, 4, 5])
        >>> plot_histogram(data)  # doctest: +SKIP
    """
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
    plt.title('Распределение оценок по математике')
    plt.xlabel('Оценка')
    plt.ylabel('Количество студентов')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_heatmap(
    matrix: np.ndarray,
    output_path: str = "plots/heatmap.png"
) -> None:
    """Построить и сохранить тепловую карту матрицы данных.

    Args:
        matrix (np.ndarray): Двумерная матрица для визуализации.
        output_path (str): Путь для сохранения изображения.

    Returns:
        None

    Raises:
        ValueError: Если matrix не является двумерным массивом.
        OSError: Если не удается сохранить файл.

    Examples:
        >>> matrix = np.array([[1, 0.5], [0.5, 1]])
        >>> plot_heatmap(matrix)  # doctest: +SKIP
    """
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    
    sns.heatmap(
        matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=False,
        linewidths=0.5,
        cbar_kws={'label': 'Корреляция'}
    )
    
    plt.title('Распределение баллов', fontsize=16, pad=20)
    plt.xlabel('Предмет')
    plt.ylabel('Оценка')
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_line(
    x: np.ndarray,
    y: np.ndarray,
    output_path: str = "plots/line_plot.png"
) -> None:
    """Построить и сохранить линейный график зависимости y от x.

    Args:
        x (np.ndarray): Значения по оси X.
        y (np.ndarray): Значения по оси Y.
        output_path (str): Путь для сохранения изображения.

    Returns:
        None

    Raises:
        ValueError: Если длины x и y не совпадают.
        OSError: Если не удается сохранить файл.

    Examples:
        >>> x = np.arange(1, 11)
        >>> y = np.random.randint(60, 100, size=10)
        >>> plot_line(x, y)  # doctest: +SKIP
    """
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    plt.plot(
        x, y,
        marker='o',
        linestyle='-',
        linewidth=2,
        markersize=6,
        markeredgewidth=1.5,
        label='Оценка по математике'
    )
    plt.title('Зависимость оценки по математике от номера студента', fontsize=16, pad=20)
    plt.xlabel('Номер студента', fontsize=12)
    plt.ylabel('Оценка', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
