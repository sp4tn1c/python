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
main_author = Author('Nikolai', 'P2345')

template = env.get_template("index.html")




class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global template
        global c_r_controller

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        print(self.path)
        url_query_dict = parse_qs(self.path.rpartition('?')[-1])
        if self.path == '/':
            # root url
            result = template.render(myapp="CurrenciesListApp",
                            navigation=[{'caption': 'Основная страница',
                                         'href': "https://nickzhukov.ru"},
                                        {'caption': 'Об авторе', 'href': '/author'}
                                        ],
                            author_name=main_author.name,
                            author_group=main_author.group,
                                     currencies= c_r_controller._read()
                                     )

        if 'currency/delete' in self.path:
            # print(self.path.rpartition('?')[-1])
            c_r_controller._delete(url_query_dict['id'][0])
            # print(user_params_dict['id'][0])

            # c_r_controller._delete(user_id = )

        if 'currency/show' in self.path:
            print(c_r_controller._read())

        if 'currency/update' in self.path:
            # localhost:8080?usd=100000.100
            if 'usd' or 'USD' in url_query_dict:
                c_r_controller._update({'USD': url_query_dict['usd'][0]})
                result = template.render(result=f'обновление {url_query_dict} завершено')



        self.end_headers()
        # result = "<html><h1>Hello, world!</h1></html>"
        self.wfile.write(bytes(result, "utf-8"))


httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('server is running')
httpd.serve_forever()
