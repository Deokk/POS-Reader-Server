from server_directory import client_thread

if __name__ == '__main__':
    s = client_thread.socket_communicator('192.168.25.43', 5001)
    s.run()
