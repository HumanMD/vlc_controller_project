import queue
import socket
import sys

from threads.ConsumerThread import ConsumerThread
from threads.ProducerThread import ProducerThread

HOST = ""
PORT = 15000
q = queue.Queue(maxsize=3)


def sub_server(address, backlog=1):
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

    threads = [ProducerThread(q, conn), ConsumerThread(q)]
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    sub_server((HOST, PORT))
