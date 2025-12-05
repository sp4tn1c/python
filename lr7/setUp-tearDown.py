from lab7 import get_currencies
import unittest
import io
import requests


class TestStreamWrite(unittest.TestCase):

  def setUp(self):
    self.nonstandardstream = io.StringIO()


    try:
        self.get_currencies = get_currencies(['USD'],
                                           url="https://",
                                           handle=self.nonstandardstream)
    except:
        self.trace = trace(get_currencies, handle=self.nonstandardstream)

def break_stream(self): # проверка сломанного потока при ошибочном API

    broken_stream = io.StringIO()
    broken_stream.write('assert_phrase_error')

    with self.assertRaises(requests.eceptions.RequestEception):
        get_currencies(['USD'], url="https://", broken_stream=broken_stream)

    regex = broken_stream.getvalue()
    self.assertRegex(regex, r'Ошибка получения API')



def test_writing_stream(self):
    
    output = self.nonstandardstream.getvalue()
    self.assertRegex(output, r"Ошибка при запросе к API")

def tearDown(self):

    del self.nonstandardstream



# Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)
