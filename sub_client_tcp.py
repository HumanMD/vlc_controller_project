import socket
import sys

HOST = "192.168.198.131"
PORT = 15000


def send_commands(s):
    while True:
        command = input("<start|stop>,<video-lan-number> -> ")
        s.sendall(command.encode())


def conn_sub_server(server_address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creation of client socket
        s.connect(server_address)  # connection to the server
        print(f"connected to the server at {server_address}")
    except socket.error as error:
        print(f"something wrong...\n {error}")
        sys.exit()
    send_commands(s)


if __name__ == "__main__":
    conn_sub_server((HOST, PORT))
