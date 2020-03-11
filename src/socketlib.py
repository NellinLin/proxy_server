import socket
from src.httpreslib import HttpResponse


def create_socket(host, port):
    new_socket = socket.socket()
    new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_socket.bind((host, port))
    new_socket.listen(10)
    return new_socket


def receive_message(sock):
    message = sock.recv(1024)

    if not message:
        raise ConnectionError()

    message = message.decode('utf-8')
    return message


def response_message(request):
    response = HttpResponse(request)
    return response.create_response()
