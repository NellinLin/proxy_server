from datetime import datetime
from urllib import parse
import urllib.request

file_path = './src/logs.txt'
max_request_logs = 500

status_types = {
    '200': 'OK',
    '403': 'Forbidden',
    '404': 'Not Found',
    '405': 'Method Not Allowed',
    '409': 'Conflict'
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
        file = open('./src/logs.txt', 'rb+')
        data = file.read().decode().split('REQUEST_LOG')[1:]
        if len(data) == 0:
            last_number = 0
        else:
            last_number = int(data[-1].split('\r\n')[0])
        file.close()

        if last_number == max_request_logs:
            args = 'wb+'
            last_number = 0
        else:
            args = 'ab+'

        file = open('./src/logs.txt', args)
        file.write('REQUEST_LOG {}\r\n'.format(last_number + 1).encode())
        file.write(self.request.encode())
        file.close()

    def get_data(self, request_list):
        return '\r\n'.join(request_list[1:])

    def find_error(self, request):
        if request.find('https://') != -1:
            return self.response_with_error(409)
        return ''

    def create_response(self):
        request_split = self.request.split('\r\n')
        self.write_request()

        request_first_line = request_split[0].split(' ')
        self.request_path = parse.unquote(request_first_line[1])
        data = self.get_data(request_split)

        find_error = self.find_error(self.request_path)
        if find_error != '':
            return find_error

        response_for_http = urllib.request.urlopen(self.request_path, data=data.encode())
        response = response_for_http.read()
        return response
