from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request, parse
import logging
import re


rates_URL = 'http://www.cbr.ru/currency_base/daily/'
currency_name = 'USD'

class CurrencyConverterHTTPServer(BaseHTTPRequestHandler):
    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info(f'GET request, \nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}\n')
        self.set_response()
        currency_rate = self.get_currency_rate()
        if currency_rate[0] is True:
            self.wfile.write(f'USD rate is {currency_rate[1]}'.encode('utf-8'))
        else:
            self.wfile.write(currency_rate[1].encode('utf-8'))

    def get_currency_rate(self, search_URL=rates_URL, search_currency=currency_name):
        req = request.Request(search_URL)
        resp = request.urlopen(req)
        respData = resp.read()
        search_pattern = search_currency + r'.*?(\d{2}[,]\d*)<\/td>'
        paragraphs = re.findall(search_pattern, str(respData))
        for line in paragraphs:
            if line:
                USD_rate = float(line.replace(',', '.'))
                return True, USD_rate
        error_msg = f'ERROR: {search_currency} rate not found.'
        return False, error_msg

def run(server_class=HTTPServer, handler_class=CurrencyConverterHTTPServer, port=8082):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    run()