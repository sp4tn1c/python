"""
Модуль контроллера пользователей для системы управления подписками на валюты.

Содержит класс UserController, реализующий паттерн Singleton для обеспечения
единого состояния данных о пользователях в течение всего времени работы приложения.
"""

from models.user import User


class UserController:
    
    """Singleton контроллер для управления пользователями и их подписками.

        Обеспечивает хранение и манипуляцию данными о пользователях системы.
        Реализует паттерн Singleton для предотвращения создания множественных
        экземпляров с рассинхронизированными данными.

        Attributes:
            users (list[User]): Список всех зарегистрированных пользователей.
            next_id (int): Следующий доступный идентификатор для нового пользователя.

        Examples:
            >>> controller = UserController()
            >>> controller.get_user(1).name
            'Алексей'
            >>> controller.add_user("Новый пользователь")
            True
            >>> controller.update_user_subscription(1, 'USD', subscribe=True)
            True
        """
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.users = [
                User(id=1, name='Алексей', subscribed_currencies=['USD', 'EUR']),
                User(id=2, name='Елизавета', subscribed_currencies=['GBP']),
                User(id=3, name='Михаил', subscribed_currencies=['USD', 'AUD'])
            ]
            self.next_id = 4
            self._initialized = True

    def get_user(self, user_id: int):
        """Получить пользователя по ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_all_users(self):
        """Получить всех пользователей"""
        return self.users

    def add_user(self, name: str):
        """Добавить нового пользователя"""
        new_user = User(id=self.next_id, name=name)
        self.users.append(new_user)
        self.next_id += 1
        return True

    def update_user_subscription(self, user_id: int, currency_code: str, subscribe: bool):
        """Обновить подписку пользователя"""
        user = self.get_user(user_id)
        if not user:
            return False

        currency_code = currency_code.upper()

        if subscribe:
            # Добавляем подписку
            user.subscribe_to_currency(currency_code)
            return True
        else:
            # Удаляем подписку
            user.unsubscribe_from_currency(currency_code)
            return True
