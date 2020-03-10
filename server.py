import threading
from src import socketlib
from src import handlers
from src.readconf import read_config_file
from multiprocessing import Process


CONFIG_PATH = '/etc/httpd.conf'
HOST = ''
PORT = 6080

def worker(listen_socket, config_data):
    thread_pool = []
    for i in range(int(int(config_data['thread_limit'])/4)):
        thread = threading.Thread(target=handlers.handler_client,
                                  args=[listen_socket],
                                  daemon=True)
        thread_pool.append(thread)
        thread.start()

    for thread in thread_pool:
        thread.join()


if __name__ == '__main__':
    listen_socket = socketlib.create_socket(HOST, PORT)
    print('Listening on {}'.format(listen_socket.getsockname()))

    config_data = read_config_file(CONFIG_PATH)

    process = []
    for i in range(int(config_data['cpu_limit'])):
        process.append(Process(target=worker, args=[listen_socket, config_data]))

    for p in process:
        p.start()

    for p in process:
        p.join()
