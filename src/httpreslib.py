from datetime import datetime
from urllib import parse
import urllib.request
# import http.client

file_path = './src/logs.txt'

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
        try:
            file = open(file_path, 'ab+')
        except FileNotFoundError:
            exit('Config file {} is not found'.format(file_path))

        file.write('REQUEST\r\n'.encode())
        file.write(self.request.encode())
        file.close()

    def get_data(self, request_list):
        # flag = False
        # output_list = []
        # for elem in request_list:
        #     if elem == '':
        #         flag = True
        #
        #     if flag == True:
        #         output_list.append(elem)
        #
        # if len(output_list) > 0:
        #     return '\r\n'.join(output_list)
        # return ''
        return '\r\n'.join(request_list[1:])

    def find_error(self, request):
        if request.find('https://') != -1:
            return self.response_with_error(409)
        return ''

    def create_response(self, client_socket):
        self.write_request()
        request_first_line = self.request.split('\r\n')[0].split(' ')

        self.request_path = parse.unquote(request_first_line[1])
        data = self.get_data(self.request.split('\r\n'))

        find_error = self.find_error(self.request_path)
        if find_error != '':
            return find_error

        response_for_http = urllib.request.urlopen(self.request_path, data=data.encode())
        response = response_for_http.read()
        return response

    def burb_repeater(self):
        print('hi!')
