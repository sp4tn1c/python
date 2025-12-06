"""
Модуль тестов для модели Currency.
Тестирует создание и валидацию данных о валюте.
"""

import unittest
from models.currency import Currency


class TestCurrency(unittest.TestCase):
    """Тесты для класса Currency."""

    def test_currency_creation(self):
        """Тест создания валюты с корректными данными."""
        currency = Currency(
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=90.5,
            nominal=1
        )

        self.assertEqual(currency.num_code, "840")
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "Доллар США")
        self.assertEqual(currency.value, 90.5)
        self.assertEqual(currency.nominal, 1)

    def test_currency_properties_readonly(self):
        """Тест, что свойства валюты только для чтения."""
        currency = Currency("978", "EUR", "Евро", 99.3, 1)

        # Проверяем чтение свойств
        self.assertEqual(currency.char_code, "EUR")
        self.assertEqual(currency.value, 99.3)

        # Проверяем, что нельзя изменить напрямую
        with self.assertRaises(AttributeError):
            currency.char_code = "USD"

        with self.assertRaises(AttributeError):
            currency.value = 100.0

    def test_currency_setters(self):
        """Тест сеттеров свойств валюты (если они есть в вашем коде)."""
        # Если в вашем классе Currency есть сеттеры, добавьте тесты для них
        # Например, если есть @char_code.setter
        pass


if __name__ == '__main__':
    unittest.main()
