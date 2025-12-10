from lab7 import get_currencies
import unittest
import requests
import io
import logging

MAX_R_VALUE = 1000


class TestGetCurrencies(unittest.TestCase):

    def test_currency_usd(self):
        currency_list = ['USD']
        currency_data = get_currencies(currency_list)

        self.assertIn(currency_list[0], currency_data)
        self.assertIsInstance(currency_data['USD'], float)
        self.assertGreaterEqual(currency_data['USD'], 0)
        self.assertLessEqual(currency_data['USD'], MAX_R_VALUE)

    def test_nonexist_code(self):
        with self.assertRaises(KeyError):
            get_currencies(['XYZ'])

    def test_get_currency_connection_error(self):
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'], url="https://f10f.com")

    def test_invalid_json_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_currencies(['USD'], url="https://httpbin.org/html")

    def test_missing_valute_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            get_currencies(['USD'], url="https://httpbin.org/json")

    def test_multiple_currencies_correct(self):
        result = get_currencies(['USD', 'EUR', 'GBP'])
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIn('GBP', result)
        self.assertIsInstance(result['USD'], float)
        self.assertIsInstance(result['EUR'], float)
        self.assertIsInstance(result['GBP'], float)

    def test_empty_currency_list(self):
        result = get_currencies([])
        self.assertEqual(result, {})

    def test_currency_type_error(self):
        with self.assertRaises(TypeError):
            get_currencies(['USD'], url="https://httpbin.org/bytes/100")


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

    def test_logging_success(self):
        @logger(handles=self.stream)
        def test_function(x):
            return x * 2

        result = test_function(5)
        self.assertEqual(result, 10)

        logs = self.stream.getvalue()
        self.assertRegex(logs, r"INFO.*Начало test_function")
        self.assertRegex(logs, r"INFO.*Конец test_function.*результат=10")
        self.assertNotIn("ERROR", logs)

    def test_logging_on_error(self):
        @logger(handles=self.stream)
        def error_function():
            raise ValueError("Test error message")

        with self.assertRaises(ValueError) as context:
            error_function()

        self.assertIn("Test error message", str(context.exception))

        logs = self.stream.getvalue()
        self.assertRegex(logs, r"ERROR.*ValueError.*Test error message")

    def test_logger_different_return_values(self):
        @logger(handles=self.stream)
        def return_none():
            return None

        @logger(handles=self.stream)
        def return_list():
            return [1, 2, 3]

        self.assertIsNone(return_none())
        self.assertEqual(return_list(), [1, 2, 3])

        logs = self.stream.getvalue()
        self.assertIn("return_none", logs)
        self.assertIn("return_list", logs)
        self.assertIn("результат=None", logs)
        self.assertIn("результат=\\[1, 2, 3\\]", logs)

    def test_logger_with_args_kwargs(self):
        @logger(handles=self.stream)
        def func_with_params(a, b, c=10):
            return a + b + c

        result = func_with_params(1, 2, c=3)
        self.assertEqual(result, 6)

        logs = self.stream.getvalue()
        self.assertIn("args=(1, 2)", logs)
        self.assertIn("kwargs={'c': 3}", logs)

    def test_logger_with_logging_module(self):
        logger_obj = logging.getLogger("test")
        logger_obj.setLevel(logging.INFO)

        handler = logging.StreamHandler(self.stream)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger_obj.addHandler(handler)

        @logger(handles=logger_obj)
        def logged_func(x):
            return x ** 2

        result = logged_func(4)
        self.assertEqual(result, 16)

        logs = self.stream.getvalue()
        self.assertIn("INFO - Начало logged_func", logs)
        self.assertIn("INFO - Конец logged_func", logs)


class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.nonstandardstream = io.StringIO()

        try:
            self.get_currencies = get_currencies(['USD'],
                                                 url="https://",
                                                 handle=self.nonstandardstream)
        except:
            self.trace = trace(get_currencies, handle=self.nonstandardstream)


def break_stream(self):  # проверка сломанного потока при ошибочном API

    broken_stream = io.StringIO()
    broken_stream.write('assert_phrase_error')

    with self.assertRaises(requests.eceptions.RequestEception):
        get_currencies(['USD'], url="https://", broken_stream=broken_stream)

    regex = broken_stream.getvalue()
    self.assertRegex(regex, r'Ошибка получения API')


def test_writing_stream(self):
    output = self.nonstandardstream.getvalue()
    self.assertRegex(output, r"Ошибка при запросе к API")


def tearDown(self):
    del self.nonstandardstream
    

unittest.main(argv=[''], verbosity=2, exit=False)
