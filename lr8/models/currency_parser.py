import functools
import requests
import sys
import io

def trace(func=None, *, handle=sys.stdout):
    print(f"decorated func: {func}, {handle}")
    if func is None:
        print('func is None')
        return lambda func: trace(func, handle=handle)
    else:
        print(f'{func.__name__}, {handle}')

    @functools.wraps(func)
    def inner(*args, **kwargs):
        handle.write(f"Using handling output\n")
        # print(func.__name__, args, kwargs)
        return func(*args, **kwargs)

    # print('return inner')
    return inner

nonstandardstream = io.StringIO()

@trace(handle=nonstandardstream)
def increm(x):
    """Инкремент"""
    # print("Инкремент")
    return x+1

increm(2)

nonstandardstream.getvalue()

class CurrencyParser:
    def __init__(self, url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
                 handle=sys.stdout):

        self.url = url
        self.handle = handle

    def get_currencies(self, currency_codes: list) -> dict:
        """
        Возвращает словарь вида:
        {'USD': 92.15, 'EUR': 100.55, ...}
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            currencies = {}

            if "Valute" in data:
                for code in currency_codes:
                    if code in data["Valute"]:
                        currencies[code] = data["Valute"][code]["Value"]
                    else:
                        currencies[code] = f"Код валюты '{code}' не найден."
            return currencies

        except requests.exceptions.RequestException as e:
            self.handle.write(f"Ошибка при запросе к API: {e}")
            return {}

    # Пример использования функции:

if __name__ == "__main__":
    parser = CurrencyParser()
    currency_list = ['USD', 'EUR', 'GBP', 'NNZ']

    result = parser.get_currencies(currency_list)
    print(result)
