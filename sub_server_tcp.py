import queue
import re
import socket
import sys
import threading
import time

HOST = ""
PORT = 15000
q = queue.Queue(maxsize=4)
initial_action = ''
current_state = [
    dict(vl=1, action=initial_action),
    dict(vl=2, action=initial_action),
    dict(vl=3, action=initial_action),
    dict(vl=4, action=initial_action)
]
current_msg = dict(vl=0, action=initial_action)
lock = threading.Lock()


def regex_check(message):
    if re.findall("^(start|stop+)(,)([1-4])$", message):
        return True


class ProducerThread(threading.Thread):
    def __init__(self, q_msg, conn):
        threading.Thread.__init__(self)
        self.q_msg = q_msg
        self.conn = conn

    def run(self):

        while True:
            data = self.conn.recv(4096)
            msg = str(data, 'utf-8')

            if msg == 'esc':
                print('closing connection')
                sys.exit()

            if not regex_check(msg):
                print('illegal input!')
                continue

            self.q_msg.put(msg, True)
            print(f"producer thread, insert: {msg}")


class ConsumerThread(threading.Thread):
    def __init__(self, q_msg):
        threading.Thread.__init__(self)
        self.q_msg = q_msg

    def run(self):
        global current_msg
        global lock

        while True:
            time.sleep(3)
            array_msg = self.q_msg.get(True).split(',')
            new_msg = {
                'vl': int(array_msg[1]),
                'action': array_msg[0]
            }
            lock.acquire()
            current_msg.update(new_msg)
            print(f"consumer thread, consuming: {current_msg} ")
            lock.release()


class VideoLanThread(threading.Thread):

    def __init__(self, name, vlan_number):
        threading.Thread.__init__(self)
        self.name = name
        self.vlan_number = vlan_number

    def run(self):
        global lock
        global current_state
        global current_msg
        while True:

            if self.vlan_number == current_msg['vl']:
                state = current_state[self.vlan_number - 1]
                if state['action'] != current_msg['action']:
                    lock.acquire()
                    state.update(current_msg)
                    current_msg.update({
                        'vl': 0,
                        'action': ''
                    })
                    print(f"thread {self.name}: {state}")
                    lock.release()


def sub_server(address, backlog=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(backlog)
        print("server initialized, listening...")
    except socket.error as error:
        print(f"something wrong ...\n {error}")
        lock.release()
        sys.exit()
    conn, client_address = s.accept()
    print(f"connection Server - Client established: {client_address} ")

    threads = [ProducerThread(q, conn), ConsumerThread(q),
               VideoLanThread('vlan1', 1), VideoLanThread('vlan2', 2),
               VideoLanThread('vlan3', 3), VideoLanThread('vlan1', 4)]
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    sub_server((HOST, PORT))
