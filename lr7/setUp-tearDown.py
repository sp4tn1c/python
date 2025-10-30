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
      pass


  def test_writing_stream(self):
    
      output = self.nonstandardstream.getvalue()

      self.assertRegex(output, r"Ошибка при запросе к API")

  def tearDown(self):

    del self.nonstandardstream



# Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)
