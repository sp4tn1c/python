"""
Модуль тестов для модели User.
Тестирует основные функции работы с пользователями и подписками.
"""

import unittest
from models.user import User


class TestUser(unittest.TestCase):
    """Тесты для класса User."""

    def test_user_creation(self):
        """Тест создания пользователя с корректными данными."""
        user = User(id=1, name="Тестовый пользователь")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Тестовый пользователь")
        self.assertEqual(user.subscribed_currencies, [])

    def test_user_creation_with_subscriptions(self):
        """Тест создания пользователя с начальными подписками."""
        user = User(id=2, name="Пользователь с подписками",
                    subscribed_currencies=['USD', 'EUR'])
        self.assertEqual(user.id, 2)
        self.assertEqual(user.name, "Пользователь с подписками")
        self.assertIn('USD', user.subscribed_currencies)
        self.assertIn('EUR', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 2)

    def test_user_creation_empty_name_fails(self):
        """Тест: создание пользователя с пустым именем вызывает ошибку."""
        with self.assertRaises(ValueError):
            User(id=3, name="")

        with self.assertRaises(ValueError):
            User(id=3, name="   ")

    def test_subscribe_to_currency(self):
        """Тест добавления подписки на валюту."""
        user = User(id=4, name="Тест подписок")

        # Добавляем первую валюту
        user.subscribe_to_currency('USD')
        self.assertIn('USD', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 1)

        # Добавляем вторую валюту
        user.subscribe_to_currency('EUR')
        self.assertIn('EUR', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 2)

        # Проверяем, что коды приводятся к верхнему регистру
        user.subscribe_to_currency('gbp')
        self.assertIn('GBP', user.subscribed_currencies)

    def test_subscribe_to_currency_idempotent(self):
        """Тест идимпотентности добавления подписки (повторное добавление не меняет список)."""
        user = User(id=5, name="Тест идимпотентности")

        user.subscribe_to_currency('USD')
        self.assertEqual(len(user.subscribed_currencies), 1)

        # Повторное добавление той же валюты
        user.subscribe_to_currency('USD')
        self.assertEqual(len(user.subscribed_currencies), 1)  # Длина не изменилась

    def test_unsubscribe_from_currency(self):
        """Тест удаления подписки на валюту."""
        user = User(id=6, name="Тест отписки", subscribed_currencies=['USD', 'EUR', 'GBP'])

        self.assertEqual(len(user.subscribed_currencies), 3)

        # Удаляем одну валюту
        user.unsubscribe_from_currency('EUR')
        self.assertNotIn('EUR', user.subscribed_currencies)
        self.assertIn('USD', user.subscribed_currencies)
        self.assertIn('GBP', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 2)

        # Проверяем, что коды приводятся к верхнему регистру
        user.unsubscribe_from_currency('gbp')
        self.assertNotIn('GBP', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 1)

    def test_unsubscribe_from_currency_idempotent(self):
        """Тест идимпотентности удаления подписки."""
        user = User(id=7, name="Тест отписки идимпотентность", subscribed_currencies=['USD'])

        # Удаляем существующую валюту
        user.unsubscribe_from_currency('USD')
        self.assertEqual(len(user.subscribed_currencies), 0)

        # Повторное удаление несуществующей валюты
        user.unsubscribe_from_currency('USD')  # Не должно вызвать ошибку
        self.assertEqual(len(user.subscribed_currencies), 0)

        # Удаление валюты, которой никогда не было
        user.unsubscribe_from_currency('EUR')  # Не должно вызвать ошибку
        self.assertEqual(len(user.subscribed_currencies), 0)

    def test_subscribed_currencies_returns_copy(self):
        """Тест, что subscribed_currencies возвращает копию списка."""
        user = User(id=8, name="Тест копии", subscribed_currencies=['USD', 'EUR'])

        original_list = user.subscribed_currencies
        original_list.append('GBP')  # Модифицируем возвращенный список

        # Внутренний список не должен измениться
        self.assertNotIn('GBP', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 2)


if __name__ == '__main__':
    unittest.main()
