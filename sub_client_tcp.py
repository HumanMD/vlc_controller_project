import socket
import sys

HOST = "192.168.65.127"
PORT = 15000


def send_commands(s):
    while True:
        command = input("-> ")
        # TODO check input syntax!
        s.sendall(command.encode())

        if command == "esc":
            print("i am closing server connection ... ")
            s.close()
            sys.exit()
        data = s.recv(4096)
        print(str(data, "utf-8"))


def conn_sub_server(server_address):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creation of client socket
        s.connect(server_address)  # connection to the server
        print(f"connected to the server at {server_address}\nto close the connection type esc")
    except socket.error as error:
        print(f"something wrong...\n {error}")
        sys.exit()
    send_commands(s)


if __name__ == "__main__":
    conn_sub_server((HOST, PORT))
