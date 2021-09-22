import socket
# import subprocess
import sys
from threading import Thread
import queue
import time
import re

HOST = ""
PORT = 15000
q = queue.Queue(maxsize=3)


def receive_commands(queue, conn):
    while True:
        data = conn.recv(4096)
        msg = str(data, 'utf-8')

        if not re.findall("^(start|stop+)(,)([1-4])$", msg):
            print('illegal action!')
            continue

        queue.put(msg, True)
        print(f"producer thread, insert: {msg}")


def consumer(queue):
    while True:
        time.sleep(2)
        msg = queue.get(True)
        print(f"consumer thread, consuming: {msg}")


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

    threads = [Thread(target=receive_commands, args=(q, conn,)), Thread(target=consumer, args=(q,))]
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    sub_server((HOST, PORT))
