from . import client_thread

if __name__ == '__main__':
    s = client_thread.socket_communicator('localhost', 5001)
    s.run()
