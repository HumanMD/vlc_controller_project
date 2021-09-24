import socket
# import subprocess
import sys
import threading
from threading import Thread
import queue
import time
import re
import datetime

HOST = ""
PORT = 15000
q = queue.Queue(maxsize=3)
threadLock = threading.Lock


def regex_check(message):
    if re.findall("^(start|stop+)(,)([1-4])$", message):
        print('illegal action!')
        return True


def classic_check(message):
    messages = message.split(',')
    actions = ['start', 'stop']
    parameters = ['1', '2', '3', '4']

    if (len(messages) == 2) \
            and \
            (any(x == messages[0] for x in actions)) \
            and \
            (any(x == messages[1] for x in parameters)):
        print('illegal action')
        return True


def producer(q_msg, conn):
    while True:
        data = conn.recv(4096)
        msg = str(data, 'utf-8')

        if msg == 'esc':
            print('closing connection')
            sys.exit()

        # COMPARE REGEX_CHECK AND CLASSIC_CHECK
        # a = datetime.datetime.now()
        # regex_check(msg)
        # b = datetime.datetime.now()
        # c = b-a
        # print(c)
        # print(f"total_seconds_delay: {c.total_seconds()}")
        # print(f"second_delay: {c.seconds}")
        # print(f"microsecond_delay: {c.microseconds}")

        if not regex_check(msg):
            print('illegal action or parameter!')
            continue

        q_msg.put(msg, True)
        print(f"producer thread, insert: {msg}")


def consumer(q_msg):
    while True:
        time.sleep(2)
        msg = q_msg.get(True)
        print(f"consumer thread, consuming: {msg}")


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

    threads = [Thread(target=producer, args=(q, conn,)), Thread(target=consumer, args=(q,))]
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    sub_server((HOST, PORT))
