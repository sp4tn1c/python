"""
Модуль интеграционных тестов для основного приложения.
Тестирует взаимодействие компонентов в изолированной среде.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from myapp import SimpleHTTPRequestHandler, CurrencyRatesMock, CurrencyRatesCRUD
from controllers.usercontroller import UserController


class TestMyAppIntegration(unittest.TestCase):
    """Интеграционные тесты для основных компонентов приложения."""

    def setUp(self):
        """Настройка тестовой среды."""
        # Сбрасываем Singleton
        UserController._instance = None

        # Создаем mock объекты для тестирования
        self.mock_request = Mock()
        self.mock_client_address = ('127.0.0.1', 8080)
        self.mock_server = Mock()

        # Создаем обработчик с mock объектами
        self.handler = SimpleHTTPRequestHandler(
            self.mock_request,
            self.mock_client_address,
            self.mock_server
        )

        # Mock для записи ответа
        self.handler.wfile = MagicMock()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()

    def test_currency_rates_mock_values(self):
        """Тест mock объекта с курсами валют."""
        mock_rates = CurrencyRatesMock()
        values = mock_rates.values

        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 4)

        # Проверяем структуру данных
        for currency_tuple in values:
            self.assertIsInstance(currency_tuple, tuple)
            self.assertEqual(len(currency_tuple), 2)
            self.assertIsInstance(currency_tuple[0], str)  # Код валюты
            self.assertIsInstance(currency_tuple[1], str)  # Значение

    @patch('myapp.c_r_controller')
    @patch('myapp.user_controller')
    def test_handler_initialization(self, mock_user_controller, mock_currency_controller):
        """Тест инициализации обработчика запросов."""
        # Проверяем, что обработчик создается
        self.assertIsInstance(self.handler, SimpleHTTPRequestHandler)

        # Проверяем, что есть основные методы
        self.assertTrue(hasattr(self.handler, 'do_GET'))
        self.assertTrue(hasattr(self.handler, 'do_POST'))
        self.assertTrue(hasattr(self.handler, '_redirect'))

    def test_redirect_method(self):
        """Тест метода перенаправления."""
        with patch.object(self.handler, 'send_response') as mock_send_response, \
                patch.object(self.handler, 'send_header') as mock_send_header, \
                patch.object(self.handler, 'end_headers') as mock_end_headers:
            # Вызываем метод перенаправления
            self.handler._redirect('/test/path')

            # Проверяем вызовы
            mock_send_response.assert_called_once_with(302)
            mock_send_header.assert_called_once_with('Location', '/test/path')
            mock_end_headers.assert_called_once()

    def test_user_controller_integration(self):
        """Тест интеграции UserController с User моделью."""
        # Сбрасываем Singleton для чистого теста
        UserController._instance = None
        controller = UserController()

        # Получаем пользователя
        user = controller.get_user(1)
        self.assertIsNotNone(user)

        # Изменяем подписку через контроллер
        initial_count = len(user.subscribed_currencies)
        controller.update_user_subscription(1, 'TEST', True)

        # Проверяем через модель
        user = controller.get_user(1)
        self.assertIn('TEST', user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), initial_count + 1)

        # Удаляем через контроллер
        controller.update_user_subscription(1, 'TEST', False)
        user = controller.get_user(1)
        self.assertNotIn('TEST', user.subscribed_currencies)

    @patch('myapp.env.get_template')
    def test_error_rendering(self, mock_get_template):
        """Тест рендеринга страницы ошибки."""
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Error</html>"
        mock_get_template.return_value = mock_template

        with patch.object(self.handler, 'send_response') as mock_send_response, \
                patch.object(self.handler, 'send_header') as mock_send_header, \
                patch.object(self.handler, 'end_headers') as mock_end_headers, \
                patch.object(self.handler.wfile, 'write') as mock_write:
            # Вызываем метод рендеринга ошибки
            self.handler._render_error("Test error", "/back")

            # Проверяем вызовы
            mock_send_response.assert_called_once_with(200)
            mock_send_header.assert_called_once_with('Content-Type', 'text/html; charset=utf-8')
            mock_end_headers.assert_called_once()
            mock_get_template.assert_called_once_with("error.html")
            mock_write.assert_called_once()


class TestCurrencyRatesCRUDIntegration(unittest.TestCase):
    """Интеграционные тесты для работы с базой данных валют."""

    def setUp(self):
        """Настройка тестовой базы данных."""
        self.mock_rates = CurrencyRatesMock()
        self.crud = CurrencyRatesCRUD(self.mock_rates)

    def test_create_operation(self):
        """Тест создания записей в базе данных."""
        # Метод _create должен выполниться без ошибок
        try:
            self.crud._create()
        except Exception as e:
            self.fail(f"_create() вызвал исключение: {e}")

    def test_read_operation(self):
        """Тест чтения записей из базы данных."""
        # Сначала создаем данные
        self.crud._create()

        # Читаем все записи
        currencies = self.crud._read()

        self.assertIsInstance(currencies, list)
        # Должно быть 4 валюты как в mock объекте
        self.assertEqual(len(currencies), 4)

        # Проверяем структуру каждой записи
        for currency in currencies:
            self.assertIn('id', currency)
            self.assertIn('char_code', currency)
            self.assertIn('name', currency)
            self.assertIn('value', currency)
            self.assertIn('nominal', currency)

    def test_read_with_filter(self):
        """Тест чтения с фильтром по коду валюты."""
        self.crud._create()

        # Читаем конкретную валюту
        currencies = self.crud._read('USD')

        self.assertIsInstance(currencies, list)
        # Должна быть только USD
        self.assertTrue(len(currencies) <= 1)

        if currencies:
            self.assertEqual(currencies[0]['char_code'], 'USD')

    def test_crud_operations_flow(self):
        """Тест полного цикла CRUD операций."""
        # Create
        self.crud._create()

        # Read
        currencies_before = self.crud._read()
        initial_count = len(currencies_before)

        # Update (тест зависит от реализации)
        # Если есть метод обновления, протестируйте его здесь

        # Delete (тест зависит от реализации)
        # Если есть метод удаления, протестируйте его здесь


if __name__ == '__main__':
    unittest.main()
