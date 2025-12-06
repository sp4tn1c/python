# models/__init__.py
# ФАЙЛ ДОЛЖЕН БЫТЬ СОЗДАН В КАТАЛОГЕ ПРОЕКТА в папке controllers

import sqlite3


class CurrencyRatesCRUD():
    def __init__(self, currency_rates_obj):
        self.__con = sqlite3.connect(':memory:')
        self.__createtable()
        self.__cursor = self.__con.cursor()
        self.__currency_rates_obj = currency_rates_obj

    def __createtable(self):
        self.__con.execute(
            "CREATE TABLE user ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL);")

        self.__con.execute("CREATE TABLE currency ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "num_code TEXT NOT NULL, "
            "char_code TEXT NOT NULL, "
            "name TEXT NOT NULL, "
            "value FLOAT, "
            "nominal INTEGER);")

        self.__con.execute("CREATE TABLE user_currency ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id INTEGER NOT NULL,"
            "currency_id INTEGER NOT NULL,"
            "FOREIGN KEY(user_id) REFERENCES user(id),"
            "FOREIGN KEY(currency_id) REFERENCES currency(id));")

        self.__con.commit()

    def _create(self):
        __params = self.__currency_rates_obj.values
        # [("USD", "90"), ("EUR", "91")]

        # Именованный стиль с правильными полями таблицы
        named_params = []
        for currency_tuple in __params:
            if len(currency_tuple) >= 2:
                # Создаем полную запись с дефолтными значениями
                named_params.append({
                    'num_code': '000',  # дефолтное значение
                    'char_code': currency_tuple[0],  # код валюты
                    'name': f'Валюта {currency_tuple[0]}',  # название
                    'value': float(currency_tuple[1]) if currency_tuple[1] else 0.0,
                    'nominal': 1  # дефолтный номинал
                })

        # Правильный запрос с полями из CREATE TABLE
        __sqlquery = '''
            INSERT INTO currency (num_code, char_code, name, value, nominal) 
            VALUES (:num_code, :char_code, :name, :value, :nominal)
        '''

        self.__cursor.executemany(__sqlquery, named_params)
        self.__con.commit()

    def _read(self, char_code: str = None):
        """Параметризованный запрос для получения валют"""
        if char_code and len(char_code) == 3:
            # Параметризованный запрос по коду
            sql = "SELECT * FROM currency WHERE char_code = ?"
            self.__cursor.execute(sql, (char_code,))
        else:
            # Все валюты
            self.__cursor.execute("SELECT * FROM currency")

        result_data = []
        for _row in self.__cursor.fetchall():
            _d = {
                'id': int(_row[0]),
                'num_code': _row[1],
                'char_code': _row[2],
                'name': _row[3],
                'value': float(_row[4]) if _row[4] else 0.0,
                'nominal': int(_row[5]) if _row[5] else 1
            }
            # Для обратной совместимости добавляем 'cur'
            _d['cur'] = _row[2]
            result_data.append(_d)

        return result_data

    def _delete(self, currency_id):
        del_statement = "DELETE FROM currency WHERE id = " + str(currency_id)
        print(del_statement)
        self.__cursor.execute(del_statement)
        self.__con.commit()

    def _update(self, currency: dict['str': float]):
        currency_code = tuple(currency.keys())[0]
        currency_value = tuple(currency.values())[0]
        upd_statement = f"UPDATE currency SET value = {currency_value} WHERE char_code = '" + str(currency_code) + "'"
        print(upd_statement)
        self.__cursor.execute(upd_statement)
        self.__con.commit()

    def __del__(self):
        self.__cursor = None
        self.__con.close()


# TODO: данный файл положить в каталог controllers, таким образом создав пакет
# каталог controllers положить в той же папке, что и app.py
# контроллер для отображения данных валют


class ViewController():


    def __init__(self, currency_rates):
        pass
        self.currency_name = currency_rates.values[0]
        self.currency_date = currency_rates.values[1]
        self.currency_value = currency_rates.values[2]


    def __call__(self):
        return f"{self.currency_name} - {self.currency_date} - {self.currency_value}"
