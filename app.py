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
            search_pattern = r'\b'+ search_currency + r'\b.*?(\d{2}[,]\d*)'
            paragraphs = re.findall(search_pattern, str(respData))
            for line in paragraphs:
                if line:
                    currency_rate = float(line.replace(',', '.'))
                    return True, currency_rate
            error_msg = f'ERROR 400: "{search_currency}" costs not found.'
        return False, error_msg


    def get_query_params(self, request_data):
        error_msg = None
        if self.command == 'GET':
            params = str(request_data).lstrip('/?').replace('&', '=').split('=')
            try:
                query_params = {
                    params[i]: params[i + 1] for i in range(0, len(params), 2)}
            except Exception as e:
                logging.error(e)
                error_msg = f'ERROR 400: Invalid request parameters.'
        elif self.command == 'POST':
            try:
                query_params = json.loads(request_data.decode('utf-8'))
            except Exception as e:
                logging.error('get_query_params method POST. ' + str(e))
                error_msg = f'ERROR 400: Invalid request parameters.'
        if error_msg:
            return False, error_msg
        elif 'favicon.ico' not in query_params:
            return True, query_params
        else:
            return None

    def get_response(self, query_params):
        response_result = list()
        for currency, quantity in query_params.items():
            currency_rate = self.get_currency_rate(currency.upper())   
            if currency_rate[0]:
                try:
                    quantity = abs(int(quantity))
                except Exception as e:
                    logging.error('get_response. ' + str(e))
                    error_msg = f'ERROR 400: Invalid value for '\
                                'the number of {currency} to transfer.'
                    return False, error_msg.encode('utf-8')
                result_value = currency_rate[1]*quantity
                response = {
                    currency: {
                        'current_rate': currency_rate[1],
                        'requested_value': quantity,
                        'result_value': result_value}}
                logging.info(f'Response value is {response}\n')
                response_result.append((json.dumps(response) + '\n').encode('utf-8'))
            else:
                logging.error(str(currency_rate[1]) + '\n')
                return False, str(currency_rate[1]).encode('utf-8')
        return True, response_result


    def do_GET(self):
        logging.info(f'GET request, \nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}\n')
        self.set_response()
        query_params = self.get_query_params(self.path)
        if query_params[0]:
            response = self.get_response(query_params[1])
            if response[0]:
                for result in response[1]:
                    self.wfile.write(result)        
            else:
                self.wfile.write(response[1])    
        elif query_params[0] == False:
            self.wfile.write(str(query_params[1]).encode('utf-8'))

    
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        logging.info(f'''POST request,\nPath: {str(self.path)}\nHeaders:
                    \n{str(self.headers)}\nBody:{post_data.decode('utf-8')}\n''')
        self.set_response()
        query_params = self.get_query_params(post_data)
        if query_params[0]:
            response = self.get_response(query_params[1])
            if response[0]:
                for result in response[1]:
                    self.wfile.write(result)        
            else:
                self.wfile.write(response[1])
        elif query_params[0] == False:
            self.wfile.write(str(query_params[1]).encode('utf-8')) 


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