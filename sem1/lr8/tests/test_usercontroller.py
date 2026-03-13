"""
Модуль тестов для контроллера пользователей UserController.
Тестирует Singleton поведение и все основные методы контроллера.
"""

import unittest
from controllers.usercontroller import UserController
from models.user import User


class TestUserController(unittest.TestCase):
    """Тесты для класса UserController."""

    def setUp(self):
        """Настройка перед каждым тестом: сброс Singleton."""
        # Сбрасываем Singleton для изоляции тестов
        UserController._instance = None
        self.controller = UserController()

    def test_singleton_pattern(self):
        """Тест паттерна Singleton (только один экземпляр)."""
        controller1 = UserController()
        controller2 = UserController()

        # Оба вызова должны возвращать один и тот же объект
        self.assertIs(controller1, controller2)

        # Проверяем, что это действительно тот же объект
        self.assertEqual(id(controller1), id(controller2))

    def test_initial_users_created(self):
        """Тест инициализации начального списка пользователей."""
        users = self.controller.get_all_users()

        # Проверяем, что есть 3 начальных пользователя
        self.assertEqual(len(users), 3)

        # Проверяем данные первого пользователя
        user1 = self.controller.get_user(1)
        self.assertIsNotNone(user1)
        self.assertEqual(user1.name, "Алексей")
        self.assertIn('USD', user1.subscribed_currencies)
        self.assertIn('EUR', user1.subscribed_currencies)

        # Проверяем данные второго пользователя
        user2 = self.controller.get_user(2)
        self.assertEqual(user2.name, "Елизавета")
        self.assertIn('GBP', user2.subscribed_currencies)

    def test_get_user_existing(self):
        """Тест получения существующего пользователя."""
        user = self.controller.get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Алексей")

    def test_get_user_nonexistent(self):
        """Тест получения несуществующего пользователя."""
        user = self.controller.get_user(999)  # Несуществующий ID
        self.assertIsNone(user)

    def test_get_user_invalid_id_type(self):
        """Тест получения пользователя с неверным типом ID."""
        with self.assertRaises(TypeError):
            self.controller.get_user("не число")  # Должен вызывать TypeError

    def test_get_all_users_returns_copy(self):
        """Тест, что get_all_users возвращает копию списка."""
        users1 = self.controller.get_all_users()
        users2 = self.controller.get_all_users()

        # Это должны быть разные объекты списка
        self.assertIsNot(users1, users2)

        # Но с одинаковым содержимым
        self.assertEqual(len(users1), len(users2))

        # Модификация одного не должна влиять на другой
        users1.append("тест")
        self.assertNotEqual(len(users1), len(self.controller.get_all_users()))

    def test_add_user_success(self):
        """Тест успешного добавления нового пользователя."""
        initial_count = len(self.controller.get_all_users())

        # Добавляем нового пользователя
        result = self.controller.add_user("Новый пользователь")
        self.assertTrue(result)

        # Проверяем, что количество пользователей увеличилось
        users = self.controller.get_all_users()
        self.assertEqual(len(users), initial_count + 1)

        # Проверяем данные нового пользователя
        new_user = self.controller.get_user(4)  # ID должен быть 4
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.id, 4)
        self.assertEqual(new_user.name, "Новый пользователь")
        self.assertEqual(new_user.subscribed_currencies, [])

    def test_add_user_empty_name_fails(self):
        """Тест: добавление пользователя с пустым именем вызывает ошибку."""
        initial_count = len(self.controller.get_all_users())

        with self.assertRaises(ValueError):
            self.controller.add_user("")  # Пустое имя

        with self.assertRaises(ValueError):
            self.controller.add_user("   ")  # Только пробелы

        # Количество пользователей не должно измениться
        self.assertEqual(len(self.controller.get_all_users()), initial_count)

    def test_add_user_with_whitespace(self):
        """Тест: пробелы в начале и конце имени обрезаются."""
        self.controller.add_user("  Иван Иванов  ")
        user = self.controller.get_user(4)
        self.assertEqual(user.name, "Иван Иванов")  # Без пробелов по краям

    def test_update_user_subscription_add_success(self):
        """Тест успешного добавления подписки пользователю."""
        user = self.controller.get_user(1)
        initial_subscriptions = len(user.subscribed_currencies)

        # Добавляем новую подписку
        result = self.controller.update_user_subscription(1, 'AUD', True)
        self.assertTrue(result)

        # Проверяем, что подписка добавилась
        user = self.controller.get_user(1)
        self.assertIn('AUD', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), initial_subscriptions + 1)

    def test_update_user_subscription_remove_success(self):
        """Тест успешного удаления подписки пользователя."""
        user = self.controller.get_user(1)
        initial_subscriptions = len(user.subscribed_currencies)

        # Удаляем существующую подписку
        result = self.controller.update_user_subscription(1, 'USD', False)
        self.assertTrue(result)

        # Проверяем, что подписка удалилась
        user = self.controller.get_user(1)
        self.assertNotIn('USD', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), initial_subscriptions - 1)

    def test_update_user_subscription_case_insensitive(self):
        """Тест: код валюты нечувствителен к регистру."""
        # Добавляем в нижнем регистре
        self.controller.update_user_subscription(1, 'aud', True)
        user = self.controller.get_user(1)
        self.assertIn('AUD', user.subscribed_currencies)  # Сохраняется в верхнем

        # Удаляем в смешанном регистре
        self.controller.update_user_subscription(1, 'Aud', False)
        user = self.controller.get_user(1)
        self.assertNotIn('AUD', user.subscribed_currencies)

    def test_update_user_subscription_nonexistent_user(self):
        """Тест обновления подписки несуществующего пользователя."""
        result = self.controller.update_user_subscription(999, 'USD', True)
        self.assertFalse(result)  # Должно вернуть False

    def test_update_user_subscription_idempotent_add(self):
        """Тест идимпотентности добавления подписки."""
        user = self.controller.get_user(2)
        initial_subscriptions = len(user.subscribed_currencies)

        # Добавляем подписку, которой нет
        self.controller.update_user_subscription(2, 'USD', True)
        user = self.controller.get_user(2)
        self.assertEqual(len(user.subscribed_currencies), initial_subscriptions + 1)

        # Повторно добавляем ту же подписку
        self.controller.update_user_subscription(2, 'USD', True)
        user = self.controller.get_user(2)
        self.assertEqual(len(user.subscribed_currencies), initial_subscriptions + 1)  # Не изменилось

    def test_update_user_subscription_idempotent_remove(self):
        """Тест идимпотентности удаления подписки."""
        user = self.controller.get_user(3)
        initial_subscriptions = len(user.subscribed_currencies)

        # Удаляем существующую подписку
        self.controller.update_user_subscription(3, 'USD', False)
        user = self.controller.get_user(3)
        self.assertEqual(len(user.subscribed_currencies), initial_subscriptions - 1)

        # Повторно удаляем ту же подписку
        self.controller.update_user_subscription(3, 'USD', False)
        user = self.controller.get_user(3)
        self.assertEqual(len(user.subscribed_currencies), initial_subscriptions - 1)  # Не изменилось

    def test_concurrent_user_ids(self):
        """Тест последовательной генерации ID пользователей."""
        # Добавляем несколько пользователей
        self.controller.add_user("Пользователь 4")
        self.controller.add_user("Пользователь 5")
        self.controller.add_user("Пользователь 6")

        # Проверяем ID
        user4 = self.controller.get_user(4)
        user5 = self.controller.get_user(5)
        user6 = self.controller.get_user(6)

        self.assertIsNotNone(user4)
        self.assertIsNotNone(user5)
        self.assertIsNotNone(user6)

        self.assertEqual(user4.id, 4)
        self.assertEqual(user5.id, 5)
        self.assertEqual(user6.id, 6)

        self.assertEqual(user4.name, "Пользователь 4")
        self.assertEqual(user5.name, "Пользователь 5")
        self.assertEqual(user6.name, "Пользователь 6")


if __name__ == '__main__':
    unittest.main()
