from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler

from models.author import Author
from models.user import User
from models.currency_parser import CurrencyParser

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

index_template = env.get_template("index.html")
users_template = env.get_template("users.html")
currencies_template = env.get_template("currencies.html")

main_author = Author("Kirichenko Denis", "P3122")

users = [User(1, "Kirichenko Denis")]

CURRENCY_LIST = ["USD", "EUR", "GBP", "JPY", "CNY"]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            html = index_template.render(
                title="Главная",
                author=main_author
            )

        elif self.path == "/users":
            html = users_template.render(
                title="Пользователи",
                users=users
            )

        elif self.path == "/currencies":
            parser = CurrencyParser()
            currencies = parser.get_currencies(CURRENCY_LIST)

            html = currencies_template.render(
                title="Курсы валют",
                currencies=currencies
            )

        else:
            self.send_error(404, "Страница не найдена")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer(("localhost", 8081), SimpleHTTPRequestHandler)
    print("Сервер запущен: http://localhost:8081")
    httpd.serve_forever()
