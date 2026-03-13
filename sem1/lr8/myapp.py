from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from controllers.databasecontroller import CurrencyRatesCRUD
from models import Author

from controllers import databasecontroller

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)


class CurrencyRatesMock():
    def __init__(self):
        self.__values = [("USD", "90"),
                         ("EUR", "91"),
                         ("GBP", '100'),
                         ("AUD", '52.8501')]

    @property
    def values(self):
        return self.__values


c_r = CurrencyRatesMock()

c_r_controller = databasecontroller.CurrencyRatesCRUD(c_r)
c_r_controller._create()
# print(c_r.values)

# main_author = author.Author('Nikolai', 'P2345')
main_author = Author('Denis Kirichenko', 'P3122')

template = env.get_template("index.html")




class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global template
        global c_r_controller

        result = ''

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        print(self.path)
        url_query_dict = parse_qs(self.path.rpartition('?')[-1])

        if self.path == '/':
            result = template.render(myapp="CurrenciesListApp",
                                     navigation=[
                                         {'caption': 'Главная', 'href': '/'},
                                         {'caption': 'Валюты', 'href': '/currencies'},
                                         {'caption': 'Пользователи', 'href': '/users'},
                                         {'caption': 'Автор', 'href': '/author'}
                                     ],
                                     author_name=main_author.name,
                                     author_group=main_author.group,
                                     currencies=c_r_controller._read()
                                     )

        elif 'currency/delete' in self.path:
            if 'id' in url_query_dict:
                c_r_controller._delete(url_query_dict['id'][0])
                self.send_response(302)
                self.send_header('Location', '/currencies')
                self.end_headers()
                return
            else:
                template = env.get_template("delete_currency.html")
                result = template.render(
                    error_message="Не указан ID валюты",
                    back_url="/currencies"
                )

        elif 'currency/show' in self.path:
            currencies = c_r_controller._read()

            console_lines = []
            console_lines.append("Курсы валют из базы данных:")
            console_lines.append("=" * 50)
            for curr in currencies:
                console_lines.append(f"{curr.get('cur', 'N/A')}: {curr.get('value', 0)}")
            console_lines.append("=" * 50)

            for line in console_lines:
                print(line)

            # Показываем HTML страницу
            template = env.get_template("console.html")
            result = template.render(
                console_output="\n".join(console_lines[1:-1])  # Без первой и последней строки
            )

        elif 'currency/update' in self.path:
            key = 'usd' if 'usd' in url_query_dict else 'USD'
            c_r_controller._update({'USD': url_query_dict[key][0]})

            template = env.get_template("update_currency.html")
            result = template.render(
                title="Обновление завершено",
                message=f"USD обновлен: {url_query_dict[key][0]}",
                back_url="/currencies"
            )

        # создали страницу об авторе
        elif '/author' == self.path:
            template = env.get_template("author.html")
            result = template.render(
                title="Об авторе",
                author_name=main_author.name,
                author_group=main_author.group
            )

        # создали страницу о пользователях (сами придумываем им имена
        elif '/users' == self.path:
            template = env.get_template("users.html")
            users_data = [
                {'id': 1, 'name': 'Алексей'},
                {'id': 2, 'name': 'Елизавета'},
                {'id': 3, 'name': 'Михаил'}
            ]
            result = template.render(
                title="Список пользователей",
                users=users_data,
                total_users=len(users_data)
            )

        elif self.path == '/user':
            user_id = url_query_dict['id'][0]
            template = env.get_template("user.html")
            user_data = {
                'id': user_id,
                'name': f'Пользователь {user_id}',
                'registration_date': '2024-01-15'
            }
            user_currencies = [
                {'id': 1, 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.5, 'nominal': 1},
                {'id': 2, 'char_code': 'EUR', 'name': 'Евро', 'value': 99.3, 'nominal': 1},
            ]

            result = template.render(
                title=f"Пользователь #{user_id}",
                user=user_data,
                currencies=user_currencies,
                total_currencies=len(user_currencies)
            )

        elif self.path == '/currencies':
            template = env.get_template("currencies.html")
            currencies_data = c_r_controller._read()

            currencies_dict = {}
            for curr in currencies_data:
                code = curr.get('cur', 'N/A')
                currencies_dict[code] = {
                    'id': curr.get('id'),
                    'price': curr.get('value', 0),
                    'name': curr.get('name', code),
                    'nominal': curr.get('nominal', 1)
                }

            result = template.render(
                title="Курсы валют",
                currencies=currencies_dict,
                total_currencies=len(currencies_data)
            )

        self.end_headers()
        # result = "<html><h1>Hello, world!</h1></html>"
        self.wfile.write(bytes(result, "utf-8"))


httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('server is running')
httpd.serve_forever()
