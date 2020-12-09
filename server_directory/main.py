from server_directory import server_pretty

if __name__ == '__main__':
    s = server_pretty.socket_communicator('localhost', 5001)
    s.run()
