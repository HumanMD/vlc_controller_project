import socket
# import subprocess
import sys

HOST = "192.168.65.127"
PORT = 15000


def receive_commands(conn):
    while True:
        data = conn.recv(4096)
        if str(data, "utf-8") == "esc":
            print("i am closing server connection ... ")
            conn.close()
            sys.exit()
        print(str(data, "utf-8"))
        conn.sendall(data)


def sub_server(address,
               backlog=1):  # il backlog è il numero di connessioni non ancora accettate ma ancora ammesse prima di rifiutarne altre
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(backlog)
        print("server initialized, listening...")
    except socket.error as error:
        print(f"something wrong ...\n {error}")
        sys.exit()
    conn, client_address = s.accept()
    print(f"connection Server - Client established: {client_address} ")
    receive_commands(conn)


if __name__ == "__main__":
    sub_server((HOST, PORT))
