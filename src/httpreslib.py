from datetime import datetime
from urllib import parse
import urllib.request
# import http.client

file_path = './src/logs.txt'

status_types = {
    '200': 'OK',
    '403': 'Forbidden',
    '404': 'Not Found',
    '405': 'Method Not Allowed'
}


class HttpResponse:
    def __init__(self, request):
        self.headers = {
            'Content-Type:': '',
            'Content-Length:': '',
            'Date:': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Server:': 'server/1.0',
            'Connection:': 'close'
        }
        self.request = request
        self.request_path = ''
        self.file_path = ''

    def add_header(self, type, body):
        self.headers.update({type: body})

    def response_with_error(self, code):
        response = 'HTTP/1.1 {} {}\r\n'.format(code, status_types[str(code)]) +\
                   '{} {}\r\n'.format('Date:', str(self.headers['Date:'])) +\
                   '{} {}\r\n'.format('Server:', str(self.headers['Server:'])) +\
                   '{} {}\r\n'.format('Connection:', str(self.headers['Connection:'])) +\
                   '\n'
        return response.encode()

    def write_request(self):
        try:
            file = open(file_path, 'ab+')
        except FileNotFoundError:
            exit('Config file {} is not found'.format(file_path))

        file.write('REQUEST\r\n'.encode())
        file.write(self.request.encode())
        file.close()

    def create_response(self, client_socket):
        self.write_request()

        request_first_line = self.request.split('\r\n')[0].split(' ')
        request_method = request_first_line[0]
        if not (request_method == 'GET' or request_method == 'HEAD'):
            return self.response_with_error(405)

        self.request_path = parse.unquote(request_first_line[1])

        response_for_http = urllib.request.urlopen(self.request_path)
        client_socket.sendall(response_for_http.read())
        client_socket.close()

    def burb_repeater(self):
        print('hi!')
