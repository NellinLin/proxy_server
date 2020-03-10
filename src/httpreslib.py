from datetime import datetime
from urllib import parse
import http.client

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

    def create_response(self):
        request_first_line = self.request.split('\r\n')[0].split(' ')

        request_method = request_first_line[0]
        if not (request_method == 'GET' or request_method == 'HEAD'):
            return self.response_with_error(405)

        self.request_path = parse.urlparse(parse.unquote(request_first_line[1]))
        url_netloc = self.request_path.netloc
        url_path = self.request_path.path

        headers_lib = {}
        for s in self.request.split('\r\n')[1:]:
            header_split = s.split(': ')
            if len(header_split) > 1:
               headers_lib[header_split[0]] = header_split[1]

        conn = http.client.HTTPConnection(url_netloc)
        conn.request(request_method, url_path, headers=headers_lib)
        response = conn.getresponse()

        print("Status: {} and reason: {}".format(response.status, response.reason), response.headers)

        new_response = response.read()
        conn.close()
        return new_response
