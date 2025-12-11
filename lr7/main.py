import requests
import json
import functools
import logging
import sys

def logger(func=None, *, handles=sys.stdout):
    """
    Декоратор для записи логов о вызовах функций.
    
    Args:
        func: Декорируемая функция
        handles: Куда писать логи (sys.stdout, файловый объект или logging.Logger)
    
    Returns:
        Обёрнутую функцию с логированием
    """
    if func is None:
        return lambda f: logger(f, handles=handles)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        is_logging = isinstance(handles, logging.Logger)
        
        if is_logging:
            handles.info(f"Начало {func.__name__}: {args}, {kwargs}")
        else:
            handles.write(f"INFO: Начало {func.__name__}: {args}, {kwargs}\n")
        
        try:
            output = func(*args, **kwargs)
            
            if is_logging:
                handles.info(f"Конец {func.__name__}: результат={output}")
            else:
                handles.write(f"INFO: Конец {func.__name__}: результат={output}\n")
            
            return output
            
        except Exception as err:
            if is_logging:
                handles.error(f"Ошибка {func.__name__}: {type(err).__name__} - {str(err)}")
            else:
                handles.write(f"ERROR: Ошибка {func.__name__}: {type(err).__name__} - {str(err)}\n")
            raise

    return wrapper

@logger(handles=sys.stdout)
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Запрашивает курсы валют с API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют ['USD', 'EUR']
        url: Адрес API
    
    Returns:
        Словарь {код: курс}
    
    Raises:
        ConnectionError: Нет связи с API
        ValueError: Неверный JSON
        KeyError: Нет ключа Valute или валюты
        TypeError: Неверный тип курса
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        raise ConnectionError("API недоступен")
    
    try:
        info = resp.json()
    except json.JSONDecodeError:
        raise ValueError("Некорректный JSON")
    
    if "Valute" not in info:
        raise KeyError('Нет ключа "Valute"')
    
    result = {}
    for code in currency_codes:
        if code not in info["Valute"]:
            raise KeyError(f'Нет валюты "{code}"')
        
        val = info["Valute"][code]
        if "Value" not in val:
            raise KeyError(f'Нет ключа "Value" для {code}')
        
        if not isinstance(val["Value"], (int, float)):
            raise TypeError(f'Неверный тип курса {code}')
        
        result[code] = val["Value"]
    
    return result

@logger(handles=sys.stdout)
def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax² + bx + c = 0
    
    Args:
        a, b, c: Коэффициенты
    
    Returns:
        Корни или None если нет решений
    
    Raises:
        TypeError: Нечисловые коэффициенты
        ValueError: Нет решений
    """
    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise TypeError("Коэффициенты должны быть числами")
    
    if a == 0:
        if b == 0:
            if c == 0:
                return None
            raise ValueError("Нет решений")
        return -c / b
    
    d = b * b - 4 * a * c
    
    if d < 0:
        return None
    elif d == 0:
        return -b / (2 * a)
    else:
        r1 = (-b + d ** 0.5) / (2 * a)
        r2 = (-b - d ** 0.5) / (2 * a)
        return (r1, r2)

def create_file_logger():
    """
    Создаёт логгер для записи в файл.
    
    Returns:
        Настроенный logging.Logger
    """
    logger_obj = logging.getLogger("file_logger")
    logger_obj.setLevel(logging.INFO)
    
    if logger_obj.handlers:
        return logger_obj
    
    handler = logging.FileHandler("app.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    
    logger_obj.addHandler(handler)
    return logger_obj

if __name__ == "__main__":
    print("Тест get_currencies")
    try:
        print(get_currencies(['USD', 'EUR']))
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\nТест solve_quadratic")
    tests = [
        (1, -5, 6),
        (1, 2, 1),
        (1, 0, 1),
        (0, 2, -4),
    ]
    
    for a, b, c in tests:
        try:
            print(f"{a}x² + {b}x + {c} = 0 -> {solve_quadratic(a, b, c)}")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    print("\nТест логирования в файл")
    file_log = create_file_logger()
    
    @logger(handles=file_log)
    def test_func(x):
        return x * 2
    
    test_func(21)
    print("Логи записаны в app.log")
