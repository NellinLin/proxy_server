from src import socketlib

def handler_client(listen_socket):
    while True:
        client_socket, client_address = listen_socket.accept()

        try:
            request = socketlib.receive_message(client_socket)
            print('{}: {}'.format(client_address, request))

            socketlib.response_message(request, client_socket)

        except (ConnectionError, BrokenPipeError):
            print('Socket error')
        finally:
            print('Closed connection to {}'.format(client_address))
            client_socket.close()
