class User:

    """Представляет пользователя системы отслеживания курсов валют.

        Инкапсулирует данные о пользователе и предоставляет методы для управления
        его подписками на различные валюты. Является моделью в паттерне MVC.

        Attributes:
            id (int): Уникальный идентификатор пользователя в системе.
            name (str): Отображаемое имя пользователя.
            subscribed_currencies (list[str]): Список кодов валют, на которые
                                              подписан пользователь.

        Example:
            >>> user = User(id=1, name="Алексей")
            >>> user.subscribe_to_currency('USD')
            >>> user.subscribe_to_currency('EUR')
            >>> print(user.subscribed_currencies)
            ['USD', 'EUR']
            >>> user.unsubscribe_from_currency('USD')
            >>> print(user.subscribed_currencies)
            ['EUR']
        """

    def __init__(self, name: str, id: int = None, subscribed_currencies: list = None):
        self.__id = id
        self.__name = name
        self.__subscribed_currencies = subscribed_currencies or []  # Только коды валют

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: int):
        if value and value > 0:
            self.__id = value
        else:
            raise ValueError("ID должен быть положительным числом")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val: str):
        if not val or len(val) < 2:
            raise ValueError("Имя пользователя слишком короткое")
        self.__name = val

    @property
    def subscribed_currencies(self):
        """Возвращает список кодов подписанных валют"""
        return self.__subscribed_currencies

    def subscribe_to_currency(self, currency_code: str):
        """Добавить валюту в подписки"""
        if currency_code not in self.__subscribed_currencies:
            self.__subscribed_currencies.append(currency_code)

    def unsubscribe_from_currency(self, currency_code: str):
        """Удалить валюту из подписок"""
        if currency_code in self.__subscribed_currencies:
            self.__subscribed_currencies.remove(currency_code)

    def __str__(self):
        return f"User {self.id}: {self.name}"

    def __repr__(self):
        return f"User({self.id}, '{self.name}')"
