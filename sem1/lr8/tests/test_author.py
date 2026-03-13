"""
Модуль тестов для модели Author.
Тестирует создание и свойства автора проекта.
"""

import unittest
from models.author import Author


class TestAuthor(unittest.TestCase):
    """Тесты для класса Author."""

    def test_author_creation_with_default_group(self):
        """Тест создания автора с группой по умолчанию."""
        author = Author("Иван Иванов")
        self.assertEqual(author.name, "Иван Иванов")
        self.assertEqual(author.group, "P3122")  # Значение по умолчанию

    def test_author_creation_with_custom_group(self):
        """Тест создания автора с указанной группой."""
        author = Author("Петр Петров", "P1234")
        self.assertEqual(author.name, "Петр Петров")
        self.assertEqual(author.group, "P1234")

    def test_author_properties_readonly(self):
        """Тест, что свойства автора только для чтения."""
        author = Author("Тестовый автор", "TEST")

        # Проверяем, что можно читать
        self.assertEqual(author.name, "Тестовый автор")
        self.assertEqual(author.group, "TEST")

        # Проверяем, что нельзя изменять напрямую
        with self.assertRaises(AttributeError):
            author.name = "Новое имя"

        with self.assertRaises(AttributeError):
            author.group = "Новая группа"


if __name__ == '__main__':
    unittest.main()
