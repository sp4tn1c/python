from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from models import Author
from currency_parser import CurrencyParser

# Настраиваем Jinja2 через FileSystemLoader
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")

# Автор
main_author = Author("Kirichenko Denis", "P3122")

# Валюты, которые показываем
CURRENCY_LIST = ["USD", "EUR", "GBP", "JPY", "CNY"]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        parser = CurrencyParser()
        currencies = parser.get_currencies(CURRENCY_LIST)

        result = template.render(
            myapp="CurrenciesListApp",
            navigation=[{'caption': 'Основная страница', 'href': "https://itmo.ru"}],
            author_name=main_author.name,
            group=main_author.group,
            currencies=currencies
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer(("localhost", 8081), SimpleHTTPRequestHandler)
    print("Сервер запущен: http://localhost:8081")
    httpd.serve_forever()
