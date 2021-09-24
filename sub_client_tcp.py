import socket
import sys

HOST = ""
PORT = 15000


# FUNCTION THAT GETS THE SOCKET INSTANCE AS PARAMETER
# TAKES AN INPUT STRING FROM THE STD-INPUT
# AND SEND IT TO THE SUB_SERVER_TCP
def send_commands(s):
    while True:
        command = input("<start|stop>,<video-lan-number> -> ")
        s.sendall(command.encode())

        if command == 'esc':
            print('closing connection')
            sys.exit()


# FUNCTION THAT CREATES THE CLIENT SOCKET
# CONNECT TO THE SERVER SOCKET
# AND CALL THE send_commands FUNCTION
# PASSING SOCKET INSTANCE
def conn_sub_server(server_address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_address)
        print(f"connected to the server at {server_address}")
    except socket.error as error:
        print(f"something wrong...\n {error}")
        sys.exit()
    send_commands(s)


if __name__ == "__main__":
    conn_sub_server((HOST, PORT))
