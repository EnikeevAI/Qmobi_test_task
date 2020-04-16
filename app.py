from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request, parse
import json
import logging
import re
import sys


rates_URL = 'http://www.cbr.ru/currency_base/daily/'


class CurrencyConverterHTTPServer(BaseHTTPRequestHandler):
    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def get_currency_rate(self, search_currency, search_URL=rates_URL):
        req = request.Request(search_URL)
        error_msg = None
        try:
            resp = request.urlopen(req)
            logging.info(f'Connecting to a url {search_URL}\n')
        except Exception as e:
            logging.error(e)
            error_msg = e
        if error_msg is None:
            respData = resp.read()
            search_pattern = search_currency + r'.*?(\d{2}[,]\d*)'
            paragraphs = re.findall(search_pattern, str(respData))
            for line in paragraphs:
                if line:
                    currency_rate = float(line.replace(',', '.'))
                    return True, currency_rate
            error_msg = f'ERROR 400: {search_currency} rate not found.'
        return False, error_msg

    def get_query_params(self, path):
        query_params = str(path).lstrip('/?').split('=')
        if 'favicon.ico' not in query_params:
            return query_params
        else:
            return None


    def do_GET(self):
        logging.info(f'GET request, \nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}\n')
        self.set_response()
        query_params = self.get_query_params(self.path)
        if query_params:
            currency_name = query_params[0]
            currency_rate = self.get_currency_rate(currency_name.upper())   
            if currency_rate[0]:
                try:
                    requested_value = abs(int(query_params[1]))
                except Exception as e:
                    logging.error(e + '\n')
                    error_msg = f"ERROR 400: {e}."
                    return self.wfile.write(str(error_msg).encode('utf-8'))
                result_value = currency_rate[1]*requested_value
                response = {
                    currency_name: {
                        'current_rate': currency_rate[1],
                        'requested_value': requested_value,
                        'result_value': result_value}}
                logging.info(f'Response value is {response}\n')
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                logging.error(str(currency_rate[1]) + '\n')
                self.wfile.write(str(currency_rate[1]).encode('utf-8'))

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