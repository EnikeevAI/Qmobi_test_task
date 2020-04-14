from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


class CurrencyConverterHTTPServer(BaseHTTPRequestHandler):
    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info(f'GET request, \nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}\n')
        self.set_response()
        self.wfile.write(f'GET request for {self.path}'.encode('utf-8'))

def run(port=8081):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = HTTPServer(server_address, CurrencyConverterHTTPServer)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    run()