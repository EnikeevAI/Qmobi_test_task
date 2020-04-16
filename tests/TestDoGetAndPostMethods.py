import json
import unittest
from urllib import request, parse


class TestDoGetMethod(unittest.TestCase):
    def test_incorrect_currency_name(self):
        response = request.urlopen('http://localhost:8082/?u=100')
        message = response.read().decode('utf-8')
        self.assertTrue('costs not found' in message)
  
    def test_incorrect_currency_value(self):
        response = request.urlopen('http://localhost:8082/?usd=abc')
        message = response.read().decode('utf-8')
        self.assertTrue('Invalid value' in message)

    def test_invalid_request_parameters(self):
        response = request.urlopen('http://localhost:8082/asd')
        message = response.read().decode('utf-8')
        self.assertTrue('Invalid request parameters' in message)

    def test_get_method_correct(self):
        response = request.urlopen('http://localhost:8082/?usd=100')
        message = response.read().decode('utf-8')
        message = json.loads(message)
        current_rate = message['usd']['current_rate']
        requested_value = message['usd']['requested_value']
        result_value = message['usd']['result_value']
        self.assertTrue(current_rate * requested_value == result_value)


class TestDoPostMethod(unittest.TestCase):
    def test_incorrect_currency_name(self):
        data = json.dumps({"u": 100}).encode()
        req = request.Request('http://localhost:8082', data=data)
        response = request.urlopen(req)
        message = response.read().decode('utf-8')
        self.assertTrue('costs not found' in message)
        
    def test_incorrect_currency_value(self):
        data = json.dumps({"usd": 'abc'}).encode()
        req = request.Request('http://localhost:8082', data=data)
        response = request.urlopen(req)
        message = response.read().decode('utf-8')
        self.assertTrue('Invalid value' in message)

    def test_post_method_correct(self):
        data = json.dumps({"usd": 100}).encode()
        req = request.Request('http://localhost:8082', data=data)
        response = request.urlopen(req)
        message = response.read().decode('utf-8')
        message = json.loads(message)
        current_rate = message['usd']['current_rate']
        requested_value = message['usd']['requested_value']
        result_value = message['usd']['result_value']
        self.assertTrue(current_rate * requested_value == result_value)


if __name__ == '__main__':
    unittest.main()


